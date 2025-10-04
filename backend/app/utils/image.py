from __future__ import annotations

from pathlib import Path
from typing import Tuple

import cv2
import numpy as np


def read_image_bytes(path: str | Path) -> np.ndarray:
    data = np.fromfile(str(path), dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Failed to read image")
    return img


def preprocess_for_ocr(image_bgr: np.ndarray) -> np.ndarray:
    # Convert to grayscale
    gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

    # Resize keeping aspect ratio so longest edge ~ 1200 px
    h, w = gray.shape[:2]
    scale = 1200.0 / max(h, w)
    if scale < 1.0:
        new_size: Tuple[int, int] = (int(w * scale), int(h * scale))
        gray = cv2.resize(gray, new_size, interpolation=cv2.INTER_AREA)

    # Denoise
    denoised = cv2.fastNlMeansDenoising(gray, h=10)

    # Adaptive threshold
    th = cv2.adaptiveThreshold(
        denoised, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 11
    )

    # Morph close to join characters
    kernel = np.ones((3, 3), np.uint8)
    closed = cv2.morphologyEx(th, cv2.MORPH_CLOSE, kernel, iterations=1)

    return closed
