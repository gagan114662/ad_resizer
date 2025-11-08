"""
Intelligent Ad Resizer - No API Required
Creates usable social media creatives using smart cropping and content-aware scaling
Uses only open-source tools: OpenCV, PIL, numpy
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance
import cv2
import numpy as np

# Social Media Platform Sizes
SOCIAL_MEDIA_SIZES = {
    # Instagram
    "instagram_feed": (1080, 1080, "Instagram Feed (Square)"),
    "instagram_story": (1080, 1920, "Instagram Story"),
    "instagram_reel": (1080, 1920, "Instagram Reel"),

    # Facebook
    "facebook_feed": (1200, 630, "Facebook Feed"),
    "facebook_story": (1080, 1920, "Facebook Story"),

    # Twitter/X
    "twitter_post": (1200, 675, "Twitter Post"),
    "twitter_header": (1500, 500, "Twitter Header"),

    # LinkedIn
    "linkedin_post": (1200, 627, "LinkedIn Post"),

    # YouTube
    "youtube_thumbnail": (1280, 720, "YouTube Thumbnail"),

    # TikTok
    "tiktok_video": (1080, 1920, "TikTok Video"),

    # Google Display Ads
    "google_display_banner": (728, 90, "Google Display Banner"),
    "google_display_medium": (300, 250, "Google Display Medium Rectangle"),
    "google_display_leaderboard": (970, 250, "Google Display Leaderboard"),
    "google_display_skyscraper": (160, 600, "Google Display Skyscraper"),
}

def detect_main_subject_saliency(image_path):
    """Detect the main subject using saliency detection"""
    img = cv2.imread(image_path)
    if img is None:
        return None

    height, width = img.shape[:2]

    try:
        # Use static saliency detection
        saliency = cv2.saliency.StaticSaliencySpectralResidual_create()
        success, saliency_map = saliency.computeSaliency(img)

        if success:
            # Threshold the saliency map
            saliency_map = (saliency_map * 255).astype("uint8")
            _, thresh_map = cv2.threshold(saliency_map, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

            # Find contours
            contours, _ = cv2.findContours(thresh_map, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                # Get the largest contour
                largest_contour = max(contours, key=cv2.contourArea)
                x, y, w, h = cv2.boundingRect(largest_contour)

                # Expand bbox slightly for better framing
                margin = 0.1
                x = max(0, int(x - w * margin))
                y = max(0, int(y - h * margin))
                w = min(width - x, int(w * (1 + 2 * margin)))
                h = min(height - y, int(h * (1 + 2 * margin)))

                center_x = x + w // 2
                center_y = y + h // 2

                return {
                    'bbox': (x, y, w, h),
                    'center': (center_x, center_y),
                    'img_size': (width, height)
                }
    except Exception as e:
        print(f"    ⚠ Saliency detection failed: {e}")

    # Fallback: assume subject is centered
    return {
        'bbox': (width // 4, height // 4, width // 2, height // 2),
        'center': (width // 2, height // 2),
        'img_size': (width, height)
    }

def create_blurred_background(img, target_width, target_height):
    """Create a blurred background from the image for padding"""
    # Resize image to target size (will be stretched)
    background = img.resize((target_width, target_height), Image.Resampling.BILINEAR)

    # Apply heavy blur
    background = background.filter(ImageFilter.GaussianBlur(radius=50))

    # Reduce brightness and saturation for a subtle background
    enhancer = ImageEnhance.Brightness(background)
    background = enhancer.enhance(0.5)

    enhancer = ImageEnhance.Color(background)
    background = enhancer.enhance(0.6)

    return background

def smart_crop_and_resize(image_path, target_width, target_height, subject_info):
    """Smart crop and resize maintaining the main subject"""
    img = Image.open(image_path)
    orig_width, orig_height = img.size

    orig_ratio = orig_width / orig_height
    target_ratio = target_width / target_height

    # Get subject information
    if subject_info:
        subject_x, subject_y, subject_w, subject_h = subject_info['bbox']
        center_x, center_y = subject_info['center']
    else:
        center_x, center_y = orig_width // 2, orig_height // 2
        subject_x, subject_y = orig_width // 4, orig_height // 4
        subject_w, subject_h = orig_width // 2, orig_height // 2

    # Strategy 1: If aspect ratios are very different, use blurred background
    if abs(orig_ratio - target_ratio) > 0.3:
        # Create canvas with blurred background
        canvas = create_blurred_background(img, target_width, target_height)

        # Calculate scaling to fit original while maintaining aspect ratio
        scale = min(target_width / orig_width, target_height / orig_height)
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)

        # Resize original image
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Calculate position to center the image
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2

        # Paste onto canvas
        if resized.mode == 'RGBA':
            canvas.paste(resized, (x_offset, y_offset), resized)
        else:
            canvas.paste(resized, (x_offset, y_offset))

        return canvas

    # Strategy 2: Smart crop focusing on subject
    else:
        # Calculate crop dimensions that match target aspect ratio
        if orig_ratio > target_ratio:
            # Original is wider - crop width
            crop_height = orig_height
            crop_width = int(crop_height * target_ratio)
        else:
            # Original is taller - crop height
            crop_width = orig_width
            crop_height = int(crop_width / target_ratio)

        # Ensure crop doesn't exceed image bounds
        crop_width = min(crop_width, orig_width)
        crop_height = min(crop_height, orig_height)

        # Position crop to keep subject centered
        crop_x = max(0, min(center_x - crop_width // 2, orig_width - crop_width))
        crop_y = max(0, min(center_y - crop_height // 2, orig_height - crop_height))

        # Perform crop
        cropped = img.crop((crop_x, crop_y, crop_x + crop_width, crop_y + crop_height))

        # Resize to target dimensions
        resized = cropped.resize((target_width, target_height), Image.Resampling.LANCZOS)

        return resized

def enhance_for_ads(img):
    """Enhance image for advertising (slightly increase contrast and saturation)"""
    # Slight contrast boost
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(1.1)

    # Slight saturation boost
    enhancer = ImageEnhance.Color(img)
    img = enhancer.enhance(1.15)

    # Slight sharpness boost
    enhancer = ImageEnhance.Sharpness(img)
    img = enhancer.enhance(1.2)

    return img

def main():
    burger_image = "/Users/gaganarora/Desktop/projects/ad_resizer/Resize_backend_mango/front-view-tasty-meat-burger-with-cheese-and-salad-free-photo.jpg"
    output_dir = Path("/Users/gaganarora/Desktop/projects/ad_resizer/intelligent_resized_ads")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("INTELLIGENT SOCIAL MEDIA AD RESIZER")
    print("Content-Aware Resizing with Smart Cropping & Blurred Backgrounds")
    print("="*70)

    # Detect main subject once
    print("\n[1/3] Analyzing image and detecting main subject...")
    subject_info = detect_main_subject_saliency(burger_image)

    if subject_info:
        bbox = subject_info['bbox']
        center = subject_info['center']
        print(f"  ✓ Subject detected at ({center[0]}, {center[1]})")
        print(f"    Bounding box: {bbox[0]}, {bbox[1]}, {bbox[2]}x{bbox[3]}")
    else:
        print(f"  ⚠ Using default centering")

    # Process each platform
    print(f"\n[2/3] Generating social media creatives...")

    total = len(SOCIAL_MEDIA_SIZES)
    successful = 0
    failed = 0

    for i, (platform_id, (width, height, display_name)) in enumerate(SOCIAL_MEDIA_SIZES.items(), 1):
        print(f"\n[{i}/{total}] {display_name} ({width}x{height})")

        output_path = output_dir / f"{platform_id}_{width}x{height}.jpg"

        try:
            # Smart crop and resize
            result_img = smart_crop_and_resize(burger_image, width, height, subject_info)

            # Enhance for advertising
            result_img = enhance_for_ads(result_img)

            # Convert to RGB if needed
            if result_img.mode == 'RGBA':
                rgb_img = Image.new('RGB', result_img.size, (255, 255, 255))
                rgb_img.paste(result_img, mask=result_img.split()[3])
                result_img = rgb_img

            # Save with high quality
            result_img.save(output_path, 'JPEG', quality=95, optimize=True)

            print(f"  ✓ Saved: {output_path.name}")
            successful += 1

        except Exception as e:
            print(f"  ❌ Failed: {e}")
            failed += 1

    # Summary
    print("\n[3/3] Processing complete!")
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Successful: {successful}/{total}")
    print(f"Failed: {failed}/{total}")
    print(f"\nOutput directory: {output_dir}")
    print("\nFeatures used:")
    print("  • Saliency detection for subject identification")
    print("  • Smart cropping to preserve main subject")
    print("  • Blurred background padding for extreme aspect ratios")
    print("  • Color enhancement for advertising appeal")

if __name__ == "__main__":
    main()
