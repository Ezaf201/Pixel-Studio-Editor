"""OpenCV filters and adjustments used by the desktop editor."""
from __future__ import annotations

import cv2
import numpy as np


def apply_edit(image: np.ndarray, settings: dict) -> np.ndarray:
    """Apply a filter and brightness/contrast adjustments to an image copy."""
    result = image.copy()
    filter_name = settings.get("filter", "original")
    if filter_name == "grayscale":
        result = cv2.cvtColor(cv2.cvtColor(result, cv2.COLOR_BGR2GRAY), cv2.COLOR_GRAY2BGR)
    elif filter_name == "sepia":
        matrix = np.array([[0.272, 0.534, 0.131], [0.349, 0.686, 0.168], [0.393, 0.769, 0.189]], dtype=np.float32)
        result = np.clip(cv2.transform(result, matrix), 0, 255).astype(np.uint8)
    elif filter_name == "blur":
        result = cv2.GaussianBlur(result, (15, 15), 0)
    elif filter_name == "sharpen":
        result = cv2.filter2D(result, -1, np.array([[0, -1, 0], [-1, 5, -1], [0, -1, 0]]))
    elif filter_name != "original":
        raise ValueError("Unknown filter selected.")
    brightness = int(np.clip(float(settings.get("brightness", 0)), -100, 100))
    contrast = float(np.clip(float(settings.get("contrast", 0)), -100, 100))
    return cv2.convertScaleAbs(result, alpha=1.0 + contrast / 100.0, beta=brightness)
