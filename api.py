import os
import io
import logging
from typing import List, Dict
from contextlib import asynccontextmanager
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from transformers import pipeline
from PIL import Image
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging (production-grade instead of print statements)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Constants
MODEL_NAME = "umm-maybe/AI-image-detector"
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

# Global model pipeline
classifier = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Modern lifespan handler (replaces deprecated @app.on_event)."""
    global classifier
    logger.info(f"Loading model: {MODEL_NAME}...")
    try:
        classifier = pipeline("image-classification", model=MODEL_NAME)
    except Exception as e:
        logger.warning(f"Online model load failed ({e}), trying offline/cached mode...")
        os.environ["TRANSFORMERS_OFFLINE"] = "1"
        os.environ["HF_HUB_OFFLINE"] = "1"
        classifier = pipeline("image-classification", model=MODEL_NAME)
    logger.info("Model loaded successfully!")
    yield
    # Cleanup on shutdown
    logger.info("Shutting down API server...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI Image Detector API",
    description="API for detecting AI-generated images using the umm-maybe/AI-image-detector model. "
                "Upload any image and get a confidence score indicating whether it's AI-generated or real.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware — properly configured (no wildcard with credentials)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Fixed: can't use True with wildcard origins
    allow_methods=["*"],
    allow_headers=["*"],
)


def validate_file(file: UploadFile, contents: bytes) -> None:
    """Validate uploaded file type and size."""
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type '{file.content_type}'. Allowed: {', '.join(allowed_types)}"
        )
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail=f"File too large ({len(contents) / 1024 / 1024:.1f}MB). Max size: {MAX_FILE_SIZE / 1024 / 1024:.0f}MB"
        )


def format_prediction(results: list, threshold: float, filename: str) -> Dict:
    """Format model output into a clean API response with verdict logic."""
    top = results[0] if results else None
    if top:
        is_ai = top["label"].lower() in ["artificial", "ai"]
        verdict = "AI Generated" if is_ai and top["score"] >= threshold else "Real"
    else:
        verdict = "Unknown"

    return {
        "filename": filename,
        "verdict": verdict,
        "confidence": round(top["score"], 4) if top else 0.0,
        "threshold_used": threshold,
        "predictions": [
            {"label": r["label"], "score": round(r["score"], 4)}
            for r in results
        ]
    }


@app.get("/")
async def root():
    """API information and available endpoints."""
    return {
        "message": "AI Image Detector API is running",
        "model": MODEL_NAME,
        "version": "1.0.0",
        "endpoints": {
            "health": "GET /health",
            "detect": "POST /detect",
            "detect_batch": "POST /detect/batch",
            "docs": "GET /docs"
        }
    }


@app.get("/health")
async def health_check():
    """Check if the API and model are ready."""
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    return {
        "status": "healthy",
        "model": MODEL_NAME,
        "ready": True
    }


@app.post("/detect")
async def detect_image(
    file: UploadFile = File(..., description="Image file (JPEG, PNG, WEBP, BMP)"),
    threshold: float = Query(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for AI detection verdict (0.0 to 1.0)"
    )
) -> Dict:
    """
    Detect if an uploaded image is AI-generated or real.

    - **file**: Image file to analyze
    - **threshold**: Confidence threshold — predictions above this are labeled "AI Generated"

    Returns classification verdict, confidence score, and detailed predictions.
    """
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    # Read and validate
    contents = await file.read()
    validate_file(file, contents)

    try:
        image = Image.open(io.BytesIO(contents)).convert("RGB")
        results = classifier(image)
        logger.info(f"Detected {file.filename}: {results[0]['label']} ({results[0]['score']:.4f})")
        return format_prediction(results, threshold, file.filename)

    except Exception as e:
        logger.error(f"Error processing {file.filename}: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")


@app.post("/detect/batch")
async def detect_images_batch(
    files: List[UploadFile] = File(..., description="List of image files (max 10)"),
    threshold: float = Query(
        default=0.5,
        ge=0.0,
        le=1.0,
        description="Confidence threshold for AI detection verdict"
    )
) -> Dict:
    """
    Detect multiple images in a batch (max 10 images).

    Returns classification results for each image individually.
    """
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")

    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch")

    results_batch = []

    for file in files:
        try:
            contents = await file.read()
            validate_file(file, contents)

            image = Image.open(io.BytesIO(contents)).convert("RGB")
            predictions = classifier(image)

            result = format_prediction(predictions, threshold, file.filename)
            result["error"] = None
            results_batch.append(result)
            logger.info(f"Batch - {file.filename}: {predictions[0]['label']} ({predictions[0]['score']:.4f})")

        except HTTPException as he:
            results_batch.append({
                "filename": file.filename,
                "error": he.detail,
                "verdict": None,
                "predictions": None
            })
        except Exception as e:
            logger.error(f"Batch error for {file.filename}: {e}")
            results_batch.append({
                "filename": file.filename,
                "error": str(e),
                "verdict": None,
                "predictions": None
            })

    return {
        "total_images": len(files),
        "successful": sum(1 for r in results_batch if r.get("error") is None),
        "failed": sum(1 for r in results_batch if r.get("error") is not None),
        "results": results_batch
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")

    logger.info(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
