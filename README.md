# Ad Resizer - Intelligent Social Media Creative Generator

An intelligent image resizing tool that uses **ClipDrop AI** to automatically adapt product images into multiple social media ad formats while maintaining the main subject and generating seamless background extensions.

## Features

✅ **AI-Powered Background Extension** - Uses ClipDrop's Uncrop API to intelligently extend images
✅ **14 Social Media Formats** - Instagram, Facebook, Twitter, LinkedIn, YouTube, TikTok, Google Ads
✅ **Subject Preservation** - Keeps your main product/subject perfectly centered
✅ **Seamless Blending** - AI-generated backgrounds blend naturally with original image
✅ **Batch Processing** - Generate all formats with a single command

## Supported Formats

### Instagram
- Feed (1080x1080)
- Story (1080x1920)
- Reel (1080x1920)

### Facebook
- Feed (1200x630)
- Story (1080x1920)

### Twitter/X
- Post (1200x675)
- Header (1500x500)

### LinkedIn
- Post (1200x627)

### YouTube
- Thumbnail (1280x720)

### TikTok
- Video (1080x1920)

### Google Display Ads
- Banner (728x90)
- Medium Rectangle (300x250)
- Leaderboard (970x250)
- Skyscraper (160x600)

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
