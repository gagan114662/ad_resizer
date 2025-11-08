# Ad Resizer - Intelligent Social Media Creative Generator

An intelligent image resizing tool that uses **ClipDrop AI** to automatically adapt product images into **66 social media ad formats** across 11 platforms while maintaining the main subject and generating seamless background extensions.

## Features

✅ **AI-Powered Background Extension** - Uses ClipDrop's Uncrop API to intelligently extend images
✅ **66 Social Media Formats** - Complete coverage of all major platforms
✅ **11 Platforms Supported** - Instagram, Facebook, Twitter/X, LinkedIn, YouTube, TikTok, Pinterest, Snapchat, Google Ads, Reddit, WhatsApp, Telegram
✅ **Subject Preservation** - Keeps your main product/subject perfectly centered
✅ **Seamless Blending** - AI-generated backgrounds blend naturally with original image
✅ **Intelligent Fallback** - Automatic fallback to smart resizing when API credits run out
✅ **Batch Processing** - Generate all formats with a single command

## Supported Platforms & Formats (66 Total)

### 📱 Instagram (8 formats)
- Feed Square (1080x1080)
- Feed Landscape (1080x566)
- Feed Vertical (1080x1350)
- Story (1080x1920)
- Reel (1080x1920)
- Carousel Square (1080x1080)
- Carousel Vertical (1080x1350)
- Profile Photo (320x320)

### 👥 Facebook (9 formats)
- Feed Square (1080x1080)
- Feed Landscape (1200x630)
- Feed Vertical (1080x1350)
- Story (1080x1920)
- Reel (1080x1920)
- Cover Photo (820x312)
- Event Image (1920x1080)
- Marketplace (1080x1080)
- Right Column Ad (254x133)

### 🐦 Twitter/X (5 formats)
- Feed Landscape (1200x675)
- Feed Square (800x800)
- Header (1500x500)
- Profile Photo (400x400)
- Card Landscape (800x418)

### 💼 LinkedIn (7 formats)
- Feed Landscape (1200x627)
- Feed Square (1080x1080)
- Feed Vertical (1080x1350)
- Story (1080x1920)
- Company Logo (300x300)
- Cover Photo (1128x191)
- Personal Banner (646x220)

### 🎥 YouTube (6 formats)
- Thumbnail (1280x720)
- Channel Art (2560x1440)
- Display Ad (300x250)
- Overlay Ad (480x70)
- Discovery Ad (1280x720)
- Shorts (1080x1920)

### 🎵 TikTok (4 formats)
- Video (1080x1920)
- In-Feed Square (1080x1080)
- In-Feed Landscape (1920x1080)
- Profile Photo (200x200)

### 📌 Pinterest (7 formats)
- Standard Pin (1000x1500)
- Square Pin (1000x1000)
- Long Pin (1000x2100)
- Infographic (1000x3000)
- Story Pin (1080x1920)
- Carousel (1000x1500)
- Collection (1000x1500)

### 👻 Snapchat (3 formats)
- Ad (1080x1920)
- Story (1080x1920)
- Collection Ad (1080x1920)

### 🎯 Google Display Ads (13 formats)
- Banner (468x60)
- Leaderboard (728x90)
- Medium Rectangle (300x250)
- Large Rectangle (336x280)
- Skyscraper (120x600)
- Wide Skyscraper (160x600)
- Half Page (300x600)
- Large Leaderboard (970x90)
- Billboard (970x250)
- Mobile Banner (320x50)
- Large Mobile Banner (320x100)
- Square (250x250)
- Small Square (200x200)

### 🔴 Reddit (2 formats)
- Feed Post (1200x628)
- Story (1080x1920)

### 💬 WhatsApp (1 format)
- Status (1080x1920)

### ✈️ Telegram (1 format)
- Post (1280x720)

## Installation

```bash
pip install pillow requests opencv-python numpy
```

## Usage

### ClipDrop API (Recommended)

1. Get your ClipDrop API key from https://clipdrop.co/apis

2. Update the API key in `resize_ads_clipdrop.py`:
```python
CLIPDROP_API_KEY = "your_api_key_here"
```

3. Update the image path:
```python
burger_image = "/path/to/your/image.jpg"
```

4. Run:
```bash
python3 resize_ads_clipdrop.py
```

### Alternative Methods

**Intelligent Resize (No API Required)**
```bash
python3 resize_ads_intelligent.py
```
Uses smart cropping, saliency detection, and blurred backgrounds.

**Adobe Firefly (Enterprise)**
```bash
python3 resize_ads_firefly.py
```
Requires Adobe Firefly API credentials (enterprise plan).

## Output

All generated images are saved in the respective output directories:
- `clipdrop_resized_ads/` - ClipDrop AI results
- `intelligent_resized_ads/` - Smart resize results
- `resized_ads_firefly/` - Adobe Firefly results

## Examples

### Input
Original product image (1470x980)

### Output
14 perfectly formatted social media creatives with:
- ✅ Main subject preserved and centered
- ✅ AI-generated background extensions
- ✅ Platform-optimized dimensions
- ✅ Professional quality

## API Comparison

| API | Quality | Cost | Speed | Recommendation |
|-----|---------|------|-------|----------------|
| ClipDrop | ⭐⭐⭐⭐⭐ | $ | Fast | **Best Choice** |
| Adobe Firefly | ⭐⭐⭐⭐⭐ | $$$ | Slow | Enterprise only |
| Intelligent (No API) | ⭐⭐⭐ | Free | Fastest | Fallback option |

## License

MIT License

## Author

Created for intelligent ad creative generation across multiple social media platforms.
