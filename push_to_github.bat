@echo off
echo ========================================
echo   AI Image Detector - Push to GitHub
echo ========================================
echo.

echo Step 1: Adding all new files...
git add api.py requirements-api.txt Dockerfile .dockerignore DEPLOYMENT.md test_api.py README.md GITHUB_DEPLOYMENT.md .github/
echo.

echo Step 2: Checking status...
git status
echo.

echo Step 3: Committing changes...
git commit -m "Add API deployment files for AI image detector - FastAPI REST API with endpoints - Docker support - Cloud deployment guides - GitHub Actions CI/CD - Updated documentation"
echo.

echo Step 4: Pushing to GitHub...
git push
echo.

echo ========================================
echo   Done! Check GitHub to verify upload
echo ========================================
pause
