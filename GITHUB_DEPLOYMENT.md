# GitHub Deployment Guide

This guide will help you push your AI Image Detector API to GitHub and set up automated deployments.

## 📤 Push to GitHub

### Step 1: Add All New Files

```bash
git add api.py requirements-api.txt Dockerfile .dockerignore DEPLOYMENT.md test_api.py README.md .github/
```

### Step 2: Commit Changes

```bash
git commit -m "Add API deployment files for AI image detector

- FastAPI REST API with single and batch detection endpoints
- Docker configuration for containerized deployment
- Comprehensive deployment guide for multiple cloud platforms
- GitHub Actions CI/CD workflow
- Updated README with API documentation
"
```

### Step 3: Push to GitHub

```bash
git push origin main
```

Or if your default branch is `master`:

```bash
git push origin master
```

---

## 🔄 First Time Setup (If Not Already Done)

If you haven't set up a GitHub repository yet:

### 1. Create Repository on GitHub

1. Go to [github.com](https://github.com)
2. Click "New repository"
3. Name it: `Ai-image-detector`
4. Don't initialize with README (you already have one)
5. Click "Create repository"

### 2. Link Local Repository

```bash
# If not already initialized
git init

# Add remote origin (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/Ai-image-detector.git

# Or if using SSH
git remote add origin git@github.com:YOUR_USERNAME/Ai-image-detector.git
```

### 3. Initial Commit and Push

```bash
git add .
git commit -m "Initial commit: AI Image Detector with API"
git branch -M main
git push -u origin main
```

---

## 🤖 GitHub Actions (Automated CI/CD)

Once pushed, GitHub Actions will automatically:

1. ✅ Test your code on every push
2. 🐳 Build Docker images
3. 🧪 Run basic validation

View the workflow status at:
```
https://github.com/YOUR_USERNAME/Ai-image-detector/actions
```

---

## 🚀 Deploy from GitHub

### Option 1: Railway (Easiest)

1. Go to [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your `Ai-image-detector` repository
4. Railway will auto-detect the Dockerfile and deploy
5. Done! Your API will be live at `https://your-app.railway.app`

### Option 2: Render

1. Go to [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Docker
   - **Health Check Path**: `/health`
5. Click "Create Web Service"

### Option 3: Google Cloud Run

```bash
# Install Google Cloud SDK first
gcloud auth login
gcloud config set project YOUR_PROJECT_ID

# Deploy directly from GitHub
gcloud run deploy ai-image-detector \
  --source https://github.com/YOUR_USERNAME/Ai-image-detector \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 4Gi
```

### Option 4: Hugging Face Spaces (FREE!)

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Docker" SDK
4. Connect your GitHub repository or upload files
5. Your API will be hosted for FREE!

---

## 🔒 Important: Secure Your .env File

**⚠️ Never commit your `.env` file to GitHub!**

Your `.gitignore` already excludes `.env`, but double-check:

```bash
# Verify .env is in .gitignore
cat .gitignore
```

For cloud deployments, add environment variables through:
- **Railway**: Settings → Variables
- **Render**: Environment → Environment Variables
- **Google Cloud Run**: Use `--set-env-vars` flag
- **Hugging Face**: Settings → Repository secrets

Example:
```bash
HF_TOKEN=hf_your_token_here
```

---

## 📊 Post-Deployment

After deploying, you'll get a public URL like:
- Railway: `https://ai-image-detector-production.up.railway.app`
- Render: `https://ai-image-detector.onrender.com`
- Cloud Run: `https://ai-image-detector-xxxxx.run.app`

Test it:
```bash
# Health check
curl https://your-deployed-url.com/health

# API docs
# Visit: https://your-deployed-url.com/docs
```

---

## 🎉 Quick Commands Summary

```bash
# Local testing
python api.py

# Commit and push
git add .
git commit -m "Your commit message"
git push origin main

# Build Docker locally
docker build -t ai-image-detector-api .
docker run -p 8000:8000 ai-image-detector-api

# Test deployed API
curl https://your-url.com/health
```

---

## 🆘 Troubleshooting

**Issue**: `git push` asks for password repeatedly
- **Solution**: Use SSH key or GitHub Personal Access Token
  - Generate token: GitHub Settings → Developer settings → Personal access tokens

**Issue**: GitHub Actions failing
- **Solution**: Check the Actions tab on GitHub for detailed logs

**Issue**: Docker build fails on cloud platform
- **Solution**: Check platform-specific logs, ensure Dockerfile is at repository root

---

## 📝 Next Steps

1. ✅ Push to GitHub
2. ✅ Deploy to your chosen platform
3. 🔒 Add API authentication (optional)
4. 📊 Set up monitoring (e.g., Sentry, Datadog)
5. 🚀 Share your API with the world!

Happy deploying! 🎉
