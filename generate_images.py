#!/usr/bin/env python3
"""
Generate AI photos for SecureStar and Harrison Financial websites
using OpenAI's gpt-image-1 model (Image Generation 2.0).

Usage:
    OPENAI_API_KEY=<your-key> python3 generate_images.py

Images are saved to:
    securestar/images/
    harrison-financial/images/
"""

import os
import base64
import time
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    raise SystemExit("openai package not installed. Run: pip install openai")


def generate_image(client: OpenAI, prompt: str, output_path: str) -> bool:
    """Generate an image using gpt-image-1 and save it."""
    print(f"  Generating: {Path(output_path).name}")
    try:
        response = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="medium",
        )
        image_bytes = base64.b64decode(response.data[0].b64_json)
        with open(output_path, "wb") as f:
            f.write(image_bytes)
        print(f"    ✓ Saved ({len(image_bytes) // 1024} KB)")
        return True
    except Exception as exc:
        print(f"    ✗ Error: {exc}")
        return False


def main() -> None:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "OPENAI_API_KEY environment variable not set.\n"
            "Export your key and re-run:\n"
            "  export OPENAI_API_KEY=sk-...\n"
            "  python3 generate_images.py"
        )

    client = OpenAI(api_key=api_key)

    ss_dir = Path("securestar/images")
    hf_dir = Path("harrison-financial/images")
    ss_dir.mkdir(parents=True, exist_ok=True)
    hf_dir.mkdir(parents=True, exist_ok=True)

    images = [
        # ── SecureStar leadership portraits ──────────────────────────────────
        {
            "file": ss_dir / "priya-nair.png",
            "prompt": (
                "Professional corporate headshot portrait of a South Asian woman in her late 30s, "
                "CEO executive. She wears a dark navy business blazer. Confident, warm expression. "
                "Soft neutral light-gray background. Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": ss_dir / "james-kowalski.png",
            "prompt": (
                "Professional corporate headshot portrait of a white man in his early 40s, "
                "CTO technology executive. He wears a navy blue dress shirt, no tie. "
                "Intelligent, thoughtful expression. Soft neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": ss_dir / "amara-reeves.png",
            "prompt": (
                "Professional corporate headshot portrait of a Black woman in her mid-30s, "
                "VP of Engineering. She wears a charcoal blazer. Confident, warm smile. "
                "Soft neutral light background. Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": ss_dir / "david-marchetti.png",
            "prompt": (
                "Professional corporate headshot portrait of a white man in his mid-50s, "
                "Chief Compliance Officer. He wears a dark suit and tie. "
                "Authoritative, trustworthy expression. Soft neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": ss_dir / "sophia-liu.png",
            "prompt": (
                "Professional corporate headshot portrait of an East Asian woman in her early 30s, "
                "machine learning researcher. She wears a smart casual blazer. "
                "Intelligent, focused expression. Soft neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": ss_dir / "marcus-torres.png",
            "prompt": (
                "Professional corporate headshot portrait of a Latino man in his late 30s, "
                "VP of Customer Engineering. He wears a business-casual button-down shirt. "
                "Friendly, approachable smile. Soft neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        # ── SecureStar office / place ─────────────────────────────────────────
        {
            "file": ss_dir / "sf-office.png",
            "prompt": (
                "Modern tech startup open-plan office interior in San Francisco. "
                "Sleek minimalist design with dark navy walls and blue accent lighting. "
                "Multiple large monitors showing data dashboards and graphs. "
                "Standing desks with developers working. Exposed industrial ceiling. "
                "Wide-angle shot, professional corporate photography, photorealistic."
            ),
        },
        # ── Harrison Financial leadership portraits ───────────────────────────
        {
            "file": hf_dir / "eleanor-harrison.png",
            "prompt": (
                "Professional corporate headshot portrait of a white woman in her early 40s, "
                "bank CEO and founder. She wears an elegant navy blue business blazer. "
                "Confident, professional smile. Clean light background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": hf_dir / "marcus-reid.png",
            "prompt": (
                "Professional corporate headshot portrait of a Black man in his late 30s, "
                "CTO of a fintech startup. He wears a dark business shirt. "
                "Confident, professional expression. Clean neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": hf_dir / "priya-nair.png",
            "prompt": (
                "Professional corporate headshot portrait of a South Asian woman in her mid-40s, "
                "Chief Risk Officer at a bank. She wears a teal-accented business blazer. "
                "Serious, professional demeanor. Clean neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": hf_dir / "james-okafor.png",
            "prompt": (
                "Professional corporate headshot portrait of a Nigerian man in his mid-30s, "
                "Chief Product Officer at a fintech company. He wears a casual blazer. "
                "Enthusiastic, approachable smile. Clean neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": hf_dir / "sarah-kwan.png",
            "prompt": (
                "Professional corporate headshot portrait of an East Asian woman in her late 30s, "
                "General Counsel and banking attorney. She wears a formal dark business suit. "
                "Composed, professional expression. Clean neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        {
            "file": hf_dir / "david-castellano.png",
            "prompt": (
                "Professional corporate headshot portrait of a Hispanic man in his early 50s, "
                "Chief Financial Officer. He wears a dark charcoal suit. "
                "Trustworthy, experienced smile. Clean neutral background. "
                "Photorealistic, studio lighting, sharp focus."
            ),
        },
        # ── Harrison Financial lifestyle / place ──────────────────────────────
        {
            "file": hf_dir / "app-lifestyle.png",
            "prompt": (
                "Young diverse professional woman in her late 20s smiling while using a "
                "mobile banking app on her smartphone. Modern bright apartment background "
                "with warm natural daylight from a window. Lifestyle photography, "
                "candid and authentic feel. Photorealistic, high quality."
            ),
        },
        {
            "file": hf_dir / "hf-office.png",
            "prompt": (
                "Modern open-plan fintech startup office. Bright, airy space with white walls "
                "and teal-blue accents. Diverse team of professionals at standing desks with "
                "monitors. Large floor-to-ceiling windows overlooking a city skyline. "
                "Professional corporate photography, wide-angle shot. Photorealistic."
            ),
        },
    ]

    print(f"Generating {len(images)} images using gpt-image-1...\n")

    print("SecureStar images:")
    securestar_images = [img for img in images if "securestar" in str(img["file"])]
    for img in securestar_images:
        generate_image(client, img["prompt"], str(img["file"]))
        time.sleep(1)

    print("\nHarrison Financial images:")
    hf_images = [img for img in images if "harrison-financial" in str(img["file"])]
    for img in hf_images:
        generate_image(client, img["prompt"], str(img["file"]))
        time.sleep(1)

    print(f"\nDone! Generated images in securestar/images/ and harrison-financial/images/")


if __name__ == "__main__":
    main()
