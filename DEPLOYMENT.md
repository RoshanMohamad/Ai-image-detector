# API Deployment Guide

This guide covers multiple ways to deploy your AI Image Detector API.

## 📋 Table of Contents
- [Local Development](#local-development)
- [Docker Deployment](#docker-deployment)
- [Cloud Deployment Options](#cloud-deployment-options)
  - [Google Cloud Run](#google-cloud-run)
  - [AWS Elastic Container Service](#aws-ecs)
  - [Azure Container Apps](#azure-container-apps)
  - [Railway](#railway)
  - [Render](#render)
  - [Hugging Face Spaces](#hugging-face-spaces)

---

## 🚀 Local Development

### 1. Install Dependencies
```bash
pip install -r requirements-api.txt
```

### 2. Run the API Server
```bash
python api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### 3. Test the API

**Using cURL:**
```bash
curl -X POST "http://localhost:8000/detect" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@path/to/your/image.jpg"
```

**Using Python:**
```python
import requests

url = "http://localhost:8000/detect"
files = {"file": open("image.jpg", "rb")}
response = requests.post(url, files=files)
print(response.json())
```

---

## 🐳 Docker Deployment

### 1. Build Docker Image
```bash
docker build -t ai-image-detector-api .
```

### 2. Run Docker Container
```bash
docker run -d -p 8000:8000 --name ai-detector ai-image-detector-api
```

### 3. Check Logs
```bash
docker logs ai-detector
```

### 4. Stop Container
```bash
docker stop ai-detector
docker rm ai-detector
```

---

## ☁️ Cloud Deployment Options

### Google Cloud Run

**Advantages:** Serverless, auto-scaling, pay-per-use

```bash
# 1. Install Google Cloud SDK
# https://cloud.google.com/sdk/docs/install

# 2. Authenticate
gcloud auth login

# 3. Set your project
gcloud config set project YOUR_PROJECT_ID

# 4. Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-image-detector

# 5. Deploy to Cloud Run
gcloud run deploy ai-image-detector \
  --image gcr.io/YOUR_PROJECT_ID/ai-image-detector \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi \
  --cpu 2
```

**Cost Estimate:** ~$0 for low traffic (generous free tier), scales based on usage

---

### AWS Elastic Container Service (ECS)

**Advantages:** Full AWS integration, highly scalable

```bash
# 1. Install AWS CLI
# https://aws.amazon.com/cli/

# 2. Configure AWS credentials
aws configure

# 3. Create ECR repository
aws ecr create-repository --repository-name ai-image-detector

# 4. Login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com

# 5. Tag and push image
docker tag ai-image-detector-api:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-image-detector:latest
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/ai-image-detector:latest

# 6. Create ECS cluster and service (use AWS Console or Terraform)
```

**Cost Estimate:** ~$30-100/month for a basic setup

---

### Azure Container Apps

**Advantages:** Simple deployment, good integration with Azure services

```bash
# 1. Install Azure CLI
# https://docs.microsoft.com/en-us/cli/azure/install-azure-cli

# 2. Login
az login

# 3. Create resource group
az group create --name ai-detector-rg --location eastus

# 4. Create container registry
az acr create --resource-group ai-detector-rg \
  --name aidetectoracr --sku Basic

# 5. Build and push
az acr build --registry aidetectoracr \
  --image ai-image-detector:latest .

# 6. Create container app environment
az containerapp env create \
  --name ai-detector-env \
  --resource-group ai-detector-rg \
  --location eastus

# 7. Deploy container app
az containerapp create \
  --name ai-image-detector \
  --resource-group ai-detector-rg \
  --environment ai-detector-env \
  --image aidetectoracr.azurecr.io/ai-image-detector:latest \
  --target-port 8000 \
  --ingress external \
  --cpu 2 --memory 4Gi
```

**Cost Estimate:** ~$30-80/month

---

### Railway (Easiest Option)

**Advantages:** Very simple, GitHub integration, great for MVPs

1. Go to [railway.app](https://railway.app)
2. Sign in with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect the Dockerfile and deploy
6. Add environment variables if needed

**Cost Estimate:** $5/month hobby plan, then usage-based

---

### Render (Simple & Affordable)

**Advantages:** Simple setup, affordable, good free tier

1. Go to [render.com](https://render.com)
2. Sign in with GitHub
3. Click "New" → "Web Service"
4. Connect your repository
5. Configure:
   - **Environment**: Docker
   - **Instance Type**: Free or Starter ($7/month)
   - **Health Check Path**: /health
6. Deploy!

**Cost Estimate:** Free tier available, or $7/month for starter

---

### Hugging Face Spaces

**Advantages:** Free hosting for ML models, great community

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Choose "Docker" as the SDK
3. Create these files in your Space:

**Dockerfile:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements-api.txt .
RUN pip install -r requirements-api.txt
COPY api.py .
EXPOSE 7860
ENV PORT=7860
CMD ["uvicorn", "api.py:app", "--host", "0.0.0.0", "--port", "7860"]
```

**README.md:**
```markdown
---
title: AI Image Detector
emoji: 🖼️
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
---
```

**Cost Estimate:** FREE! ✨

---

## 🔧 Environment Variables

For production deployments, set these environment variables:

```bash
# Optional: HuggingFace token for private models
HF_TOKEN=your_token_here

# Optional: Custom host and port
HOST=0.0.0.0
PORT=8000
```

---

## 📊 Performance Tips

1. **Use GPU instances** for faster inference:
   - Add `device=0` to pipeline initialization in `api.py`
   - Use GPU-enabled Docker base image: `nvidia/cuda:11.8.0-runtime-ubuntu22.04`

2. **Implement caching** for repeated requests

3. **Use load balancers** for high traffic

4. **Monitor with tools** like:
   - Prometheus + Grafana
   - Datadog
   - New Relic

---

## 🧪 Testing Your Deployed API

Once deployed, test with:

```python
import requests

# Replace with your deployed URL
API_URL = "https://your-api-url.com"

# Test health endpoint
health = requests.get(f"{API_URL}/health")
print(health.json())

# Test detection
files = {"file": open("test_image.jpg", "rb")}
response = requests.post(f"{API_URL}/detect", files=files)
print(response.json())
```

---

## 📝 Next Steps

1. **Add authentication** (API keys, OAuth)
2. **Implement rate limiting**
3. **Add request logging and monitoring**
4. **Set up CI/CD pipelines**
5. **Scale based on traffic patterns**

---

## 🆘 Troubleshooting

**Issue:** Model takes too long to load
- **Solution:** Use model caching, pre-load model in Docker image

**Issue:** Out of memory errors
- **Solution:** Increase container memory (4GB+ recommended)

**Issue:** Cold starts on serverless platforms
- **Solution:** Use provisioned concurrency or keep-alive requests

---

Happy deploying! 🚀
