
"""
画像処理ユーティリティ
画像変換、フォーマット処理などのヘルパー関数
"""

import cv2
import numpy as np
from PIL import Image

class ImageUtils:
    """
    画像処理ユーティリティクラス
    """
    @staticmethod
    def pil_to_cv2(pil_image: Image.Image) -> np.ndarray:
        if pil_image.mode == 'RGB':
            cv_image = np.array(pil_image)
            return cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)
        elif pil_image.mode == 'RGBA':
            cv_image = np.array(pil_image)
            return cv2.cvtColor(cv_image, cv2.COLOR_RGBA2BGRA)
        else:
            rgb_image = pil_image.convert('RGB')
            cv_image = np.array(rgb_image)
            return cv2.cvtColor(cv_image, cv2.COLOR_RGB2BGR)

    @staticmethod
    def cv2_to_pil(cv_image: np.ndarray) -> Image.Image:
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        return Image.fromarray(rgb_image)

    @staticmethod
    def ensure_rgb(image: Image.Image) -> Image.Image:
        if image.mode != 'RGB':
            return image.convert('RGB')
        return image

    @staticmethod
    def resize_with_aspect_ratio(image: Image.Image, max_width: int, max_height: int) -> Image.Image:
        width, height = image.size
        ratio = min(max_width / width, max_height / height)
        if ratio < 1:
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            return image.resize((new_width, new_height), Image.Resampling.LANCZOS)
        return image

    @staticmethod
    def apply_brightness(image: Image.Image, brightness: int) -> Image.Image:
        if brightness == 0:
            return image
        cv_image = ImageUtils.pil_to_cv2(image)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        brightness_factor = 1.0 + (brightness / 100.0)
        v = cv2.multiply(v, brightness_factor)
        v = np.clip(v, 0, 255).astype(np.uint8)
        hsv = cv2.merge([h, s, v])
        adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return ImageUtils.cv2_to_pil(adjusted)

    @staticmethod
    def apply_contrast(image: Image.Image, contrast: int) -> Image.Image:
        if contrast == 0:
            return image
        cv_image = ImageUtils.pil_to_cv2(image)
        contrast_factor = 1.0 + (contrast / 100.0)
        adjusted = cv2.convertScaleAbs(cv_image, alpha=contrast_factor, beta=0)
        return ImageUtils.cv2_to_pil(adjusted)

    @staticmethod
    def apply_saturation(image: Image.Image, saturation: int) -> Image.Image:
        if saturation == 0:
            return image
        cv_image = ImageUtils.pil_to_cv2(image)
        hsv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        saturation_factor = 1.0 + (saturation / 100.0)
        s = cv2.multiply(s, saturation_factor)
        s = np.clip(s, 0, 255).astype(np.uint8)
        hsv = cv2.merge([h, s, v])
        adjusted = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return ImageUtils.cv2_to_pil(adjusted)

    @staticmethod
    def apply_gamma_correction(image: Image.Image, gamma: float) -> Image.Image:
        if gamma == 1.0:
            return image
        cv_image = ImageUtils.pil_to_cv2(image)
        inv_gamma = 1.0 / gamma
        table = np.array([((i / 255.0) ** inv_gamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
        adjusted = cv2.LUT(cv_image, table)
        return ImageUtils.cv2_to_pil(adjusted)

    @staticmethod
    def apply_histogram_equalization(image: Image.Image) -> Image.Image:
        cv_image = ImageUtils.pil_to_cv2(image)
        yuv = cv2.cvtColor(cv_image, cv2.COLOR_BGR2YUV)
        yuv[:,:,0] = cv2.equalizeHist(yuv[:,:,0])
        adjusted = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR)
        return ImageUtils.cv2_to_pil(adjusted)

    @staticmethod
    def apply_gaussian_blur(image: Image.Image, blur_strength: int) -> Image.Image:
        if blur_strength == 0:
            return image
        cv_image = ImageUtils.pil_to_cv2(image)
        kernel_size = blur_strength * 2 + 1
        blurred = cv2.GaussianBlur(cv_image, (kernel_size, kernel_size), 0)
        return ImageUtils.cv2_to_pil(blurred)

    @staticmethod
    def get_image_info(image: Image.Image) -> dict:
        if not image:
            return {}
        return {
            'width': image.width,
            'height': image.height,
            'mode': image.mode,
            'format': image.format,
            'size_mb': (image.width * image.height * len(image.getbands())) / (1024 * 1024)
        }
