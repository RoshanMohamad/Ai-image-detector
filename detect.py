import os
import sys
import tkinter as tk
from tkinter import filedialog
from dotenv import load_dotenv
from transformers import pipeline
from huggingface_hub import InferenceClient

# Load environment variables from .env file
load_dotenv()

MODEL_NAME = "umm-maybe/AI-image-detector"

def classify_local(image_path):
    """
    Runs image classification using the model downloaded locally.
    Corresponds to Notebook Cell 2.
    """
    print(f"Loading local pipeline for {MODEL_NAME}...")
    # This will download the model the first time it runs
    pipe = pipeline("image-classification", model=MODEL_NAME)
    
    print(f"Analyzing {image_path}...")
    result = pipe(image_path)
    return result

def classify_api(image_path):
    """
    Runs image classification using the Hugging Face Inference API.
    Corresponds to Notebook Cell 6.
    """
    token = os.getenv("HF_TOKEN")
    if not token or token == "your_hugging_face_token_here":
        print("Warning: HF_TOKEN not found or not set in .env file. Skipping API inference.")
        return None
    
    print(f"Using Inference API for {MODEL_NAME}...")
    client = InferenceClient(provider="auto", api_key=token)
    
    try:
        # The API expects a file path or URL
        output = client.image_classification(image_path, model=MODEL_NAME)
        return output
    except Exception as e:
        print(f"API Error: {e}")
        return None

def pick_file():
    """Opens a file dialog to select an image."""
    root = tk.Tk()
    root.attributes('-topmost', True)  # Make the window appear on top
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.webp"), ("All files", "*.*")]
    )
    root.destroy()
    return file_path

if __name__ == "__main__":
    # Handle command line arguments for image path
    if len(sys.argv) < 2:
        print("No image path provided.")
        choice = input("Select file (y), enter path (p), or use default (d)? [y/p/d]: ").strip().lower()
        
        if choice == 'y':
            image_path = pick_file()
            if not image_path:
                print("No file selected. Exiting.")
                sys.exit()
        elif choice == 'p':
            image_path = input("Enter image path or URL: ").strip()
            if not image_path:
                print("No path provided. Exiting.")
                sys.exit()
        else:
            # Default example if no arg provided
            default_image = "https://huggingface.co/datasets/huggingface/documentation-images/resolve/main/hub/parrots.png"
            print(f"Using default example: {default_image}")
            image_path = default_image
    else:
        image_path = sys.argv[1]

    # 1. Local Inference (Robust, runs on your machine)
    print("\n--- Local Inference ---")
    try:
        local_results = classify_local(image_path)
        print("Local Result:", local_results)
    except Exception as e:
        print(f"Local Inference Failed: {e}")

    # 2. API Inference (Optional, requires Token)
    print("\n--- API Inference ---")
    api_results = classify_api(image_path)
    if api_results:
        print("API Result:", api_results)
