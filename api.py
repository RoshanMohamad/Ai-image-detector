import os
import io
from typing import List, Dict
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from transformers import pipeline
from PIL import Image
import uvicorn

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI(
    title="AI Image Detector API",
    description="API for detecting AI-generated images using the umm-maybe/AI-image-detector model",
    version="1.0.0"
)

# CORS middleware - configure as needed
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this in production to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model pipeline
MODEL_NAME = "umm-maybe/AI-image-detector"
classifier = None

@app.on_event("startup")
async def load_model():
    """Load the model on startup to avoid loading on every request."""
    global classifier
    print(f"Loading model: {MODEL_NAME}...")
    classifier = pipeline("image-classification", model=MODEL_NAME)
    print("Model loaded successfully!")

@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "AI Image Detector API is running",
        "model": MODEL_NAME,
        "endpoints": {
            "health": "/health",
            "detect": "/detect (POST)",
            "detect_batch": "/detect/batch (POST)",
            "docs": "/docs"
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
async def detect_image(file: UploadFile = File(...)) -> Dict:
    """
    Detect if an uploaded image is AI-generated or real.
    
    Args:
        file: Image file (JPEG, PNG, WEBP, BMP)
        
    Returns:
        JSON with classification results
    """
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    # Validate file type
    allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/bmp"]
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid file type. Allowed types: {', '.join(allowed_types)}"
        )
    
    try:
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Run inference
        results = classifier(image)
        
        # Format response
        return {
            "filename": file.filename,
            "predictions": results,
            "top_prediction": results[0] if results else None
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")

@app.post("/detect/batch")
async def detect_images_batch(files: List[UploadFile] = File(...)) -> Dict:
    """
    Detect multiple images in a batch.
    
    Args:
        files: List of image files
        
    Returns:
        JSON with classification results for each image
    """
    if classifier is None:
        raise HTTPException(status_code=503, detail="Model not loaded yet")
    
    if len(files) > 10:
        raise HTTPException(status_code=400, detail="Maximum 10 images per batch")
    
    results_batch = []
    
    for file in files:
        try:
            # Validate file type
            allowed_types = ["image/jpeg", "image/jpg", "image/png", "image/webp", "image/bmp"]
            if file.content_type not in allowed_types:
                results_batch.append({
                    "filename": file.filename,
                    "error": "Invalid file type",
                    "predictions": None
                })
                continue
            
            # Read and process image
            contents = await file.read()
            image = Image.open(io.BytesIO(contents))
            
            # Run inference
            predictions = classifier(image)
            
            results_batch.append({
                "filename": file.filename,
                "predictions": predictions,
                "top_prediction": predictions[0] if predictions else None,
                "error": None
            })
            
        except Exception as e:
            results_batch.append({
                "filename": file.filename,
                "error": str(e),
                "predictions": None
            })
    
    return {
        "total_images": len(files),
        "results": results_batch
    }

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.getenv("PORT", 8000))
    host = os.getenv("HOST", "0.0.0.0")
    
    print(f"Starting API server on {host}:{port}")
    uvicorn.run(app, host=host, port=port)
