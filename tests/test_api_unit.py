"""
Unit tests for AI Image Detector API.
Run with: python -m pytest tests/ -v
"""
import io
import pytest
from unittest.mock import patch, MagicMock
from PIL import Image
from fastapi.testclient import TestClient

# Mock the transformers pipeline BEFORE importing api
with patch("transformers.pipeline") as mock_pipeline:
    mock_classifier = MagicMock()
    mock_classifier.return_value = [
        {"label": "artificial", "score": 0.95},
        {"label": "human", "score": 0.05}
    ]
    mock_pipeline.return_value = mock_classifier
    
    from api import app
    import api
    api.classifier = mock_classifier

client = TestClient(app)


def create_test_image(format="JPEG") -> bytes:
    """Create a minimal test image in memory."""
    img = Image.new("RGB", (100, 100), color="red")
    buffer = io.BytesIO()
    img.save(buffer, format=format)
    buffer.seek(0)
    return buffer.read()


# ─── Root Endpoint Tests ────────────────────────────────────────────

class TestRootEndpoint:
    def test_root_returns_200(self):
        response = client.get("/")
        assert response.status_code == 200

    def test_root_contains_model_name(self):
        response = client.get("/")
        data = response.json()
        assert data["model"] == "umm-maybe/AI-image-detector"

    def test_root_contains_endpoints(self):
        response = client.get("/")
        data = response.json()
        assert "endpoints" in data
        assert "health" in data["endpoints"]
        assert "detect" in data["endpoints"]


# ─── Health Endpoint Tests ──────────────────────────────────────────

class TestHealthEndpoint:
    def test_health_returns_200_when_model_loaded(self):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_shows_ready(self):
        response = client.get("/health")
        data = response.json()
        assert data["status"] == "healthy"
        assert data["ready"] is True

    def test_health_returns_503_when_no_model(self):
        original = api.classifier
        api.classifier = None
        response = client.get("/health")
        assert response.status_code == 503
        api.classifier = original  # restore


# ─── Detection Endpoint Tests ──────────────────────────────────────

class TestDetectEndpoint:
    def test_detect_with_valid_image(self):
        image_bytes = create_test_image()
        response = client.post(
            "/detect",
            files={"file": ("test.jpg", image_bytes, "image/jpeg")}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["filename"] == "test.jpg"
        assert "verdict" in data
        assert "confidence" in data
        assert "predictions" in data

    def test_detect_returns_verdict(self):
        image_bytes = create_test_image()
        response = client.post(
            "/detect",
            files={"file": ("test.jpg", image_bytes, "image/jpeg")}
        )
        data = response.json()
        assert data["verdict"] in ["AI Generated", "Real"]

    def test_detect_with_threshold(self):
        image_bytes = create_test_image()
        response = client.post(
            "/detect?threshold=0.99",
            files={"file": ("test.jpg", image_bytes, "image/jpeg")}
        )
        data = response.json()
        assert data["threshold_used"] == 0.99

    def test_detect_no_file_returns_422(self):
        response = client.post("/detect")
        assert response.status_code == 422

    def test_detect_invalid_file_type(self):
        response = client.post(
            "/detect",
            files={"file": ("test.txt", b"not an image", "text/plain")}
        )
        assert response.status_code == 400

    def test_detect_png_image(self):
        image_bytes = create_test_image(format="PNG")
        response = client.post(
            "/detect",
            files={"file": ("test.png", image_bytes, "image/png")}
        )
        assert response.status_code == 200

    def test_detect_invalid_threshold_too_high(self):
        image_bytes = create_test_image()
        response = client.post(
            "/detect?threshold=1.5",
            files={"file": ("test.jpg", image_bytes, "image/jpeg")}
        )
        assert response.status_code == 422

    def test_detect_invalid_threshold_negative(self):
        image_bytes = create_test_image()
        response = client.post(
            "/detect?threshold=-0.1",
            files={"file": ("test.jpg", image_bytes, "image/jpeg")}
        )
        assert response.status_code == 422


# ─── Batch Detection Endpoint Tests ─────────────────────────────────

class TestBatchDetectEndpoint:
    def test_batch_detect_multiple_images(self):
        image1 = create_test_image()
        image2 = create_test_image()
        response = client.post(
            "/detect/batch",
            files=[
                ("files", ("img1.jpg", image1, "image/jpeg")),
                ("files", ("img2.jpg", image2, "image/jpeg")),
            ]
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_images"] == 2
        assert data["successful"] == 2
        assert data["failed"] == 0

    def test_batch_detect_mixed_valid_invalid(self):
        image = create_test_image()
        response = client.post(
            "/detect/batch",
            files=[
                ("files", ("good.jpg", image, "image/jpeg")),
                ("files", ("bad.txt", b"not image", "text/plain")),
            ]
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_images"] == 2
        assert data["successful"] == 1
        assert data["failed"] == 1


# ─── Validation Tests ───────────────────────────────────────────────

class TestValidation:
    def test_file_size_limit(self):
        """Test that files over 10MB are rejected."""
        # Create a file that's just over 10MB
        large_content = b"x" * (10 * 1024 * 1024 + 1)
        response = client.post(
            "/detect",
            files={"file": ("large.jpg", large_content, "image/jpeg")}
        )
        assert response.status_code == 413
