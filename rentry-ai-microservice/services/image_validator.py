import cv2
import numpy as np

def validate_image_quality(image_path):
    try:
        # Load the image using OpenCV
        img = cv2.imread(image_path)
        
        if img is None:
            return {"valid": False, "reason": "Image file not found at this path"}

        # Convert to Grayscale for analysis
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 1. BLUR CHECK: Laplacian Variance
        # Sharp images have high variance; blurry ones have low variance.
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        # 2. BRIGHTNESS CHECK: Mean Pixel Intensity
        # 0 = Pitch Black, 255 = Pure White
        brightness_score = np.mean(gray)

        # Logic Gates
        # is_blurry = blur_score < 100
        # Changed this from 100 to 300 to be more strict
        is_blurry = blur_score < 400
        is_too_dark = brightness_score < 40

  # what if the image is too light?
  # fix the logic here because if one of the conditions is met it returns without checking the others
        is_too_light = brightness_score > 200
        if is_too_light:
            return {"valid": False, "reason": "Image is too light", "score": round(brightness_score, 2)}

        if is_blurry:
            return {"valid": False, "reason": "Image is too blurry", "score": round(blur_score, 2)}
        if is_too_dark:
            return {"valid": False, "reason": "Image is too dark", "score": round(brightness_score, 2)}

        return {
            "valid": True, 
            "reason": "Quality check passed",
            "blur_score": round(blur_score, 2),
            "brightness_score": round(brightness_score, 2)
        }
    except Exception as e:
        return {"valid": False, "reason": f"System error: {str(e)}"}