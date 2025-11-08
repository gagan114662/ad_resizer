"""
Intelligent Ad Resizer using ClipDrop API
Uses ClipDrop's Uncrop API to extend images intelligently for different aspect ratios
"""

import os
import requests
from pathlib import Path
from PIL import Image
import time

# ClipDrop API Configuration
CLIPDROP_API_KEY = "a84083be14cc9a40b2a38521e17671728b1e50a16369316d5ee12488c59343e9af49a9b0f7926fb3f83d97c83b9d2c44"

# ClipDrop API Endpoints
UNCROP_URL = "https://clipdrop-api.co/uncrop/v1"
REIMAGINE_URL = "https://clipdrop-api.co/reimagine/v1/reimagine"

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

def calculate_extend_parameters(orig_width, orig_height, target_width, target_height):
    """
    Calculate how much to extend in each direction
    ClipDrop Uncrop expects extension parameters
    """
    orig_ratio = orig_width / orig_height
    target_ratio = target_width / target_height

    # Calculate scaling factor to fit original in target
    scale = min(target_width / orig_width, target_height / orig_height)

    # Calculate new dimensions after scaling
    scaled_width = int(orig_width * scale)
    scaled_height = int(orig_height * scale)

    # Calculate padding needed
    extend_left = (target_width - scaled_width) // 2
    extend_right = target_width - scaled_width - extend_left
    extend_top = (target_height - scaled_height) // 2
    extend_bottom = target_height - scaled_height - extend_top

    return {
        'scale': scale,
        'extend_left': max(0, extend_left),
        'extend_right': max(0, extend_right),
        'extend_top': max(0, extend_top),
        'extend_bottom': max(0, extend_bottom),
        'needs_extension': (extend_left > 0 or extend_right > 0 or extend_top > 0 or extend_bottom > 0)
    }

def resize_with_clipdrop_uncrop(image_path, target_width, target_height, output_path):
    """
    Use ClipDrop Uncrop API to extend image to target dimensions
    """
    img = Image.open(image_path)
    orig_width, orig_height = img.size

    # Calculate extension parameters
    params = calculate_extend_parameters(orig_width, orig_height, target_width, target_height)

    # If no extension needed, just resize
    if not params['needs_extension']:
        print(f"    → Simple resize (no extension needed)")
        resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
        resized.save(output_path, 'JPEG', quality=95, optimize=True)
        return True

    # First, scale the image to fit within target while maintaining aspect ratio
    scaled_width = int(orig_width * params['scale'])
    scaled_height = int(orig_height * params['scale'])

    if scaled_width != orig_width or scaled_height != orig_height:
        print(f"    → Scaling image to {scaled_width}x{scaled_height}")
        img = img.resize((scaled_width, scaled_height), Image.Resampling.LANCZOS)

        # Save scaled version temporarily
        temp_scaled = output_path.parent / f"temp_scaled_{output_path.name}"
        img.save(temp_scaled, 'JPEG', quality=95)
        image_to_extend = temp_scaled
    else:
        image_to_extend = image_path

    # Use ClipDrop Uncrop API
    print(f"    → Extending with ClipDrop (L:{params['extend_left']}, R:{params['extend_right']}, T:{params['extend_top']}, B:{params['extend_bottom']})")

    try:
        with open(image_to_extend, 'rb') as f:
            files = {
                'image_file': ('image.jpg', f, 'image/jpeg')
            }

            data = {
                'extend_left': str(params['extend_left']),
                'extend_right': str(params['extend_right']),
                'extend_up': str(params['extend_top']),
                'extend_down': str(params['extend_bottom'])
            }

            headers = {
                'x-api-key': CLIPDROP_API_KEY
            }

            response = requests.post(
                UNCROP_URL,
                files=files,
                data=data,
                headers=headers,
                timeout=120
            )

            if response.status_code == 200:
                # Save the extended image
                with open(output_path, 'wb') as out:
                    out.write(response.content)

                # Clean up temp file
                if image_to_extend != image_path and os.path.exists(image_to_extend):
                    os.remove(image_to_extend)

                return True
            else:
                print(f"    ❌ ClipDrop API Error: {response.status_code}")
                print(f"       Response: {response.text}")

                # Clean up temp file
                if image_to_extend != image_path and os.path.exists(image_to_extend):
                    os.remove(image_to_extend)

                return False

    except Exception as e:
        print(f"    ❌ Exception: {e}")

        # Clean up temp file
        if image_to_extend != image_path and os.path.exists(image_to_extend):
            os.remove(image_to_extend)

        return False

def fallback_smart_resize(image_path, target_width, target_height, output_path):
    """
    Fallback method: Smart resize with padding
    """
    try:
        img = Image.open(image_path)
        orig_width, orig_height = img.size

        # Calculate scaling
        scale = min(target_width / orig_width, target_height / orig_height)
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)

        # Resize image
        resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Create canvas
        canvas = Image.new('RGB', (target_width, target_height), (255, 255, 255))

        # Center the resized image
        x_offset = (target_width - new_width) // 2
        y_offset = (target_height - new_height) // 2

        canvas.paste(resized, (x_offset, y_offset))
        canvas.save(output_path, 'JPEG', quality=95, optimize=True)

        return True

    except Exception as e:
        print(f"    ❌ Fallback failed: {e}")
        return False

def main():
    burger_image = "/Users/gaganarora/Desktop/projects/ad_resizer/Resize_backend_mango/front-view-tasty-meat-burger-with-cheese-and-salad-free-photo.jpg"
    output_dir = Path("/Users/gaganarora/Desktop/projects/ad_resizer/clipdrop_resized_ads")
    output_dir.mkdir(parents=True, exist_ok=True)

    print("="*70)
    print("CLIPDROP AI-POWERED AD RESIZER")
    print("Intelligent Image Extension for Social Media Formats")
    print("="*70)

    # Get original image dimensions
    img = Image.open(burger_image)
    orig_width, orig_height = img.size
    print(f"\nOriginal image: {orig_width}x{orig_height}")

    print(f"\n[1/2] Processing {len(SOCIAL_MEDIA_SIZES)} social media formats...")

    total = len(SOCIAL_MEDIA_SIZES)
    successful = 0
    failed = 0
    used_clipdrop = 0
    used_fallback = 0

    for i, (platform_id, (width, height, display_name)) in enumerate(SOCIAL_MEDIA_SIZES.items(), 1):
        print(f"\n[{i}/{total}] {display_name} ({width}x{height})")

        output_path = output_dir / f"{platform_id}_{width}x{height}.jpg"

        # Try ClipDrop first
        success = resize_with_clipdrop_uncrop(burger_image, width, height, output_path)

        if success:
            print(f"  ✓ Saved: {output_path.name}")
            successful += 1
            used_clipdrop += 1

            # Rate limiting - wait between API calls
            time.sleep(2)
        else:
            # Fallback to smart resize
            print(f"    → Trying fallback method...")
            success = fallback_smart_resize(burger_image, width, height, output_path)

            if success:
                print(f"  ✓ Saved (fallback): {output_path.name}")
                successful += 1
                used_fallback += 1
            else:
                failed += 1

    # Summary
    print("\n[2/2] Processing complete!")
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total formats: {total}")
    print(f"Successful: {successful}/{total}")
    print(f"  - ClipDrop API: {used_clipdrop}")
    print(f"  - Fallback: {used_fallback}")
    print(f"Failed: {failed}/{total}")
    print(f"\nOutput directory: {output_dir}")

if __name__ == "__main__":
    main()
