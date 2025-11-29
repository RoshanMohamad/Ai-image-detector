# AI Image Detector Project

This project is a conversion of the `AI_image_detector.ipynb` notebook into a Python script. It uses the `umm-maybe/AI-image-detector` model to classify images.

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Configure Token (Optional)**:
    If you want to use the Hugging Face API (InferenceClient), open the `.env` file and paste your token:
    ```text
    HF_TOKEN=hf_xxxxxxxxxxxxxxxxxxx
    ```
    *Note: The local pipeline method works without a token for public models.*

## Usage

Run the script with an image path or URL:

```bash
python detect.py path/to/your/image.jpg
```

Or run it without arguments to use a default example image:

```bash
python detect.py
```
