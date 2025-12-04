"""
Test script for the AI Image Detector API
"""
import requests
import sys

def test_api(api_url="http://localhost:8000", image_path=None):
    """Test the API endpoints."""
    
    print(f"Testing API at: {api_url}\n")
    
    # 1. Test root endpoint
    print("1. Testing root endpoint...")
    try:
        response = requests.get(f"{api_url}/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # 2. Test health endpoint
    print("2. Testing health endpoint...")
    try:
        response = requests.get(f"{api_url}/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}\n")
    except Exception as e:
        print(f"   Error: {e}\n")
    
    # 3. Test detection endpoint
    if image_path:
        print(f"3. Testing detection with image: {image_path}...")
        try:
            with open(image_path, "rb") as f:
                files = {"file": (image_path, f, "image/jpeg")}
                response = requests.post(f"{api_url}/detect", files=files)
            print(f"   Status: {response.status_code}")
            print(f"   Response: {response.json()}\n")
        except Exception as e:
            print(f"   Error: {e}\n")
    else:
        print("3. Skipping detection test (no image provided)\n")
    
    print("✅ API testing complete!")

if __name__ == "__main__":
    api_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    image_path = sys.argv[2] if len(sys.argv) > 2 else None
    
    test_api(api_url, image_path)
