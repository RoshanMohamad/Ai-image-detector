# AI Image Detector 🔍🤖

![CI](https://github.com/RoshanMohamad/Ai-image-detector/workflows/Build%20and%20Test%20API/badge.svg)
![Python](https://img.shields.io/badge/python-3.10-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688)
![License](https://img.shields.io/badge/license-MIT-green)
![HuggingFace](https://img.shields.io/badge/🤗%20Model-AI--image--detector-yellow)

> Detect AI-generated images (DALL-E, Midjourney, Stable Diffusion, etc.) using a Vision Transformer model. Production-ready REST API with Docker support and CI/CD.

---

## 🚀 Features

- **REST API** — FastAPI server with interactive Swagger docs
- **Single & Batch Detection** — Analyze 1 image or up to 10 at once
- **Configurable Threshold** — Control AI detection sensitivity (0.0–1.0)
- **CLI Tool** — Command-line interface with file picker
- **Docker Ready** — Containerized deployment with health checks
- **CI/CD** — GitHub Actions pipeline with linting and testing
- **Cloud Deploy** — Guides for Railway, Render, GCP, AWS, Azure, HuggingFace Spaces

---

## 📋 Quick Start

### 1. Install Dependencies

```bash
# For API server
pip install -r requirements-api.txt

# For CLI tool only
pip install -r requirements.txt
```

### 2. Run the API Server

```bash
python api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### 3. Try It Out

**cURL:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@your_image.jpg"
```

**Python:**
```python
import requests

files = {"file": open("image.jpg", "rb")}
response = requests.post("http://localhost:8000/detect", files=files)
print(response.json())
```

---

## 📡 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check (model ready?) |
| `/detect` | POST | Detect single image |
| `/detect/batch` | POST | Detect multiple images (max 10) |
| `/docs` | GET | Interactive Swagger documentation |

### Example Response

```json
{
  "filename": "suspicious_photo.jpg",
  "verdict": "AI Generated",
  "confidence": 0.9847,
  "threshold_used": 0.5,
  "predictions": [
    {"label": "artificial", "score": 0.9847},
    {"label": "human", "score": 0.0153}
  ]
}
```

### Confidence Threshold

Control detection sensitivity with the `threshold` query parameter:

```bash
# Strict detection — only flag high-confidence AI images
curl -X POST "http://localhost:8000/detect?threshold=0.9" -F "file=@image.jpg"

# Lenient detection — flag anything suspicious
curl -X POST "http://localhost:8000/detect?threshold=0.3" -F "file=@image.jpg"
```

---

## 💻 CLI Tool

```bash
# Analyze a local file
python detect.py path/to/image.jpg

# Interactive mode (file picker)
python detect.py
```

---

## 🐳 Docker

```bash
# Build
docker build -t ai-image-detector-api .

# Run
docker run -d -p 8000:8000 ai-image-detector-api

# Check health
curl http://localhost:8000/health
```

---

## ☁️ Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions:

| Platform | Cost | Difficulty |
|----------|------|------------|
| [Hugging Face Spaces](DEPLOYMENT.md#hugging-face-spaces) | **FREE** | Easy |
| [Railway](DEPLOYMENT.md#railway) | $5/mo | Easy |
| [Render](DEPLOYMENT.md#render) | Free–$7/mo | Easy |
| [Google Cloud Run](DEPLOYMENT.md#google-cloud-run) | Pay-per-use | Medium |
| [AWS ECS](DEPLOYMENT.md#aws-ecs) | $30–100/mo | Advanced |
| [Azure Container Apps](DEPLOYMENT.md#azure-container-apps) | $30–80/mo | Advanced |

---

## 📁 Project Structure

```
Ai-image-detector/
├── api.py                 # FastAPI REST API server
├── detect.py              # CLI tool for image detection
├── test_api.py            # API integration test script
├── requirements.txt       # CLI dependencies
├── requirements-api.txt   # API dependencies
├── Dockerfile             # Container configuration
├── .dockerignore          # Docker build exclusions
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── DEPLOYMENT.md          # Cloud deployment guide
├── GITHUB_DEPLOYMENT.md   # GitHub push & deploy guide
└── README.md              # This file
```

---

## 🔧 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `HF_TOKEN` | — | HuggingFace API token (optional for public models) |
| `HOST` | `0.0.0.0` | API server host |
| `PORT` | `8000` | API server port |

---

## 📊 Model Information

- **Model**: [umm-maybe/AI-image-detector](https://huggingface.co/umm-maybe/AI-image-detector)
- **Architecture**: Vision Transformer (ViT)
- **Task**: Binary Image Classification (AI vs Real)
- **Framework**: HuggingFace Transformers (PyTorch)
- **Input**: Any image (JPEG, PNG, WebP, BMP)
- **Output**: Probability scores for "artificial" and "human"

---

## 🧪 Testing

```bash
# Test API endpoints
python test_api.py

# Test deployed API
python test_api.py https://your-deployed-url.com

# Test with a specific image
python test_api.py http://localhost:8000 path/to/image.jpg
```

---

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
