# AI Image Detector Project

This project uses the `umm-maybe/AI-image-detector` model to classify images as AI-generated or real.

## 🚀 Features

- **CLI Tool**: Command-line interface for image detection
- **REST API**: Production-ready FastAPI server
- **Docker Support**: Containerized deployment
- **Cloud Ready**: Deploy to multiple cloud platforms

## 📋 Setup

### 1. Install Dependencies

**For CLI Tool:**
```bash
pip install -r requirements.txt
```

**For API Server:**
```bash
pip install -r requirements-api.txt
```

### 2. Configure Token (Optional)
If you want to use the Hugging Face API, create a `.env` file:
```text
HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxx
```
*Note: The local pipeline method works without a token for public models.*

## 💻 Usage

### CLI Tool

Run the script with an image path or URL:

```bash
python detect.py path/to/your/image.jpg
```

Or run without arguments to use a default example:

```bash
python detect.py
```

### API Server

#### Start the Server:
```bash
python api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

#### API Endpoints:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information |
| `/health` | GET | Health check |
| `/detect` | POST | Detect single image |
| `/detect/batch` | POST | Detect multiple images (up to 10) |
| `/docs` | GET | Interactive API documentation |

#### Example Usage:

**Python:**
```python
import requests

# Single image detection
files = {"file": open("image.jpg", "rb")}
response = requests.post("http://localhost:8000/detect", files=files)
print(response.json())
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

**JavaScript/Fetch:**
```javascript
const formData = new FormData();
formData.append('file', fileInput.files[0]);

fetch('http://localhost:8000/detect', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

## 🐳 Docker Deployment

### Build and Run:
```bash
# Build the image
docker build -t ai-image-detector-api .

# Run the container
docker run -d -p 8000:8000 ai-image-detector-api
```

## ☁️ Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions on deploying to:
- Google Cloud Run
- AWS ECS
- Azure Container Apps
- Railway (Easiest!)
- Render (Affordable)
- Hugging Face Spaces (FREE!)

## 🧪 Testing

Test the API using the provided test script:

```bash
# Test API endpoints
python test_api.py

# Test with an image
python test_api.py http://localhost:8000 path/to/image.jpg
```

## 📁 Project Structure

```
.
├── detect.py              # CLI tool for image detection
├── api.py                 # FastAPI server
├── test_api.py           # API testing script
├── requirements.txt       # CLI dependencies
├── requirements-api.txt   # API dependencies
├── Dockerfile            # Docker configuration
├── .dockerignore         # Docker build exclusions
├── DEPLOYMENT.md         # Deployment guide
├── .env                  # Environment variables (create this)
└── README.md             # This file
```

## 🔧 Environment Variables

- `HF_TOKEN`: Hugging Face API token (optional)
- `HOST`: API server host (default: 0.0.0.0)
- `PORT`: API server port (default: 8000)

## 📊 Model Information

- **Model**: [umm-maybe/AI-image-detector](https://huggingface.co/umm-maybe/AI-image-detector)
- **Task**: Image Classification
- **Framework**: Transformers (PyTorch)

## 🤝 Contributing

Feel free to open issues or submit pull requests!

## 📄 License

This project is open source and available under the MIT License.
