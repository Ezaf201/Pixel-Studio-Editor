# Pixel Studio

A lightweight desktop photo editor built with Python, Tkinter, and OpenCV.

## Features

- Open and preview PNG, JPG, JPEG, WEBP, and BMP images
- Apply original, monochrome, sepia, blur, or sharpen effects
- Adjust brightness and contrast
- Reset edits and export as PNG, JPEG, or WEBP
- Process images locally on your device

## Run locally

1. Create and activate a Python virtual environment (recommended).
2. Install dependencies: `pip install -r requirements.txt`.
3. Launch the app: `python main.py`.

Tkinter is included with most Python installations. On some Linux distributions, install the system `python3-tk` package if Tkinter is missing.

## Project structure

```text
photo-editor/
├── main.py                  # Tkinter desktop interface and application entry point
├── requirements.txt         # OpenCV, NumPy, and Pillow dependencies
├── README.md                # Project overview and setup instructions
└── image_editor/
    ├── __init__.py
    └── filters.py           # OpenCV image filters and adjustments
```
