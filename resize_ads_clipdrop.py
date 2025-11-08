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

# Social Media Platform Sizes (Complete 2025 Specifications)
SOCIAL_MEDIA_SIZES = {
    # ========== INSTAGRAM ==========
    "instagram_feed_square": (1080, 1080, "Instagram Feed (Square 1:1)"),
    "instagram_feed_landscape": (1080, 566, "Instagram Feed (Landscape 1.91:1)"),
    "instagram_feed_vertical": (1080, 1350, "Instagram Feed (Vertical 4:5)"),
    "instagram_story": (1080, 1920, "Instagram Story (9:16)"),
    "instagram_reel": (1080, 1920, "Instagram Reel (9:16)"),
    "instagram_carousel_square": (1080, 1080, "Instagram Carousel (Square 1:1)"),
    "instagram_carousel_vertical": (1080, 1350, "Instagram Carousel (Vertical 4:5)"),
    "instagram_profile_photo": (320, 320, "Instagram Profile Photo"),

    # ========== FACEBOOK ==========
    "facebook_feed_square": (1080, 1080, "Facebook Feed (Square 1:1)"),
    "facebook_feed_landscape": (1200, 630, "Facebook Feed (Landscape 1.91:1)"),
    "facebook_feed_vertical": (1080, 1350, "Facebook Feed (Vertical 4:5)"),
    "facebook_story": (1080, 1920, "Facebook Story (9:16)"),
    "facebook_reel": (1080, 1920, "Facebook Reel (9:16)"),
    "facebook_cover_photo": (820, 312, "Facebook Cover Photo"),
    "facebook_event_image": (1920, 1080, "Facebook Event Image"),
    "facebook_marketplace": (1080, 1080, "Facebook Marketplace (1:1)"),
    "facebook_right_column": (254, 133, "Facebook Right Column Ad"),

    # ========== TWITTER/X ==========
    "twitter_feed_landscape": (1200, 675, "Twitter/X Feed (16:9)"),
    "twitter_feed_square": (800, 800, "Twitter/X Feed (Square 1:1)"),
    "twitter_header": (1500, 500, "Twitter/X Header (3:1)"),
    "twitter_profile_photo": (400, 400, "Twitter/X Profile Photo"),
    "twitter_card_landscape": (800, 418, "Twitter/X Card (1.91:1)"),

    # ========== LINKEDIN ==========
    "linkedin_feed_landscape": (1200, 627, "LinkedIn Feed (1.91:1)"),
    "linkedin_feed_square": (1080, 1080, "LinkedIn Feed (Square 1:1)"),
    "linkedin_feed_vertical": (1080, 1350, "LinkedIn Feed (Vertical 4:5)"),
    "linkedin_story": (1080, 1920, "LinkedIn Story (9:16)"),
    "linkedin_company_logo": (300, 300, "LinkedIn Company Logo"),
    "linkedin_cover_photo": (1128, 191, "LinkedIn Cover Photo"),
    "linkedin_banner": (646, 220, "LinkedIn Personal Banner"),

    # ========== YOUTUBE ==========
    "youtube_thumbnail": (1280, 720, "YouTube Thumbnail (16:9)"),
    "youtube_channel_art": (2560, 1440, "YouTube Channel Art"),
    "youtube_display_ad": (300, 250, "YouTube Display Ad"),
    "youtube_overlay_ad": (480, 70, "YouTube Overlay Ad"),
    "youtube_discovery_ad": (1280, 720, "YouTube Discovery Ad"),
    "youtube_short": (1080, 1920, "YouTube Shorts (9:16)"),

    # ========== TIKTOK ==========
    "tiktok_video": (1080, 1920, "TikTok Video (9:16)"),
    "tiktok_in_feed_square": (1080, 1080, "TikTok In-Feed (Square 1:1)"),
    "tiktok_in_feed_landscape": (1920, 1080, "TikTok In-Feed (Landscape 16:9)"),
    "tiktok_profile_photo": (200, 200, "TikTok Profile Photo"),

    # ========== PINTEREST ==========
    "pinterest_standard": (1000, 1500, "Pinterest Standard Pin (2:3)"),
    "pinterest_square": (1000, 1000, "Pinterest Square Pin (1:1)"),
    "pinterest_long": (1000, 2100, "Pinterest Long Pin (1:2.1)"),
    "pinterest_infographic": (1000, 3000, "Pinterest Infographic"),
    "pinterest_story": (1080, 1920, "Pinterest Story Pin (9:16)"),
    "pinterest_carousel": (1000, 1500, "Pinterest Carousel (2:3)"),
    "pinterest_collection": (1000, 1500, "Pinterest Collection (2:3)"),

    # ========== SNAPCHAT ==========
    "snapchat_ad": (1080, 1920, "Snapchat Ad (9:16)"),
    "snapchat_story": (1080, 1920, "Snapchat Story (9:16)"),
    "snapchat_collection_ad": (1080, 1920, "Snapchat Collection Ad (9:16)"),

    # ========== GOOGLE DISPLAY ADS ==========
    "google_banner": (468, 60, "Google Banner"),
    "google_leaderboard": (728, 90, "Google Leaderboard"),
    "google_medium_rectangle": (300, 250, "Google Medium Rectangle"),
    "google_large_rectangle": (336, 280, "Google Large Rectangle"),
    "google_skyscraper": (120, 600, "Google Skyscraper"),
    "google_wide_skyscraper": (160, 600, "Google Wide Skyscraper"),
    "google_half_page": (300, 600, "Google Half Page"),
    "google_large_leaderboard": (970, 90, "Google Large Leaderboard"),
    "google_billboard": (970, 250, "Google Billboard"),
    "google_mobile_banner": (320, 50, "Google Mobile Banner"),
    "google_large_mobile_banner": (320, 100, "Google Large Mobile Banner"),
    "google_square": (250, 250, "Google Square"),
    "google_small_square": (200, 200, "Google Small Square"),

    # ========== REDDIT ==========
    "reddit_feed": (1200, 628, "Reddit Feed Post"),
    "reddit_story": (1080, 1920, "Reddit Story (9:16)"),

    # ========== WHATSAPP ==========
    "whatsapp_status": (1080, 1920, "WhatsApp Status (9:16)"),

    # ========== TELEGRAM ==========
    "telegram_post": (1280, 720, "Telegram Post (16:9)"),
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
    print("     Using ClipDrop AI for intelligent background extension")

    total = len(SOCIAL_MEDIA_SIZES)
    successful = 0
    failed = 0
    skipped_no_credits = 0

    for i, (platform_id, (width, height, display_name)) in enumerate(SOCIAL_MEDIA_SIZES.items(), 1):
        print(f"\n[{i}/{total}] {display_name} ({width}x{height})")

        output_path = output_dir / f"{platform_id}_{width}x{height}.jpg"

        # Check if file already exists
        if output_path.exists():
            print(f"  ⏭  Already exists: {output_path.name}")
            successful += 1
            continue

        # Use ClipDrop API
        success = resize_with_clipdrop_uncrop(burger_image, width, height, output_path)

        if success:
            print(f"  ✓ Saved: {output_path.name}")
            successful += 1

            # Rate limiting - wait between API calls
            time.sleep(2)
        else:
            # Check if it's a credits issue
            print(f"  ⚠ Skipped (likely insufficient credits)")
            skipped_no_credits += 1
            failed += 1

    # Summary
    print("\n[2/2] Processing complete!")
    print("="*70)
    print("SUMMARY")
    print("="*70)
    print(f"Total formats: {total}")
    print(f"Successful: {successful}/{total}")
    print(f"Failed/Skipped: {failed}/{total}")
    if skipped_no_credits > 0:
        print(f"\n⚠ {skipped_no_credits} formats skipped due to insufficient ClipDrop credits")
        print("  Add credits to your ClipDrop account and run again to generate remaining formats")
    print(f"\nOutput directory: {output_dir}")

if __name__ == "__main__":
    main()
