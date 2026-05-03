#!/usr/bin/env python3
"""
Generate realistic AI photos for SecureStar and Harrison Financial websites
using OpenAI's gpt-image-2 model.

Usage:
    OPENAI_API_KEY=<your-key> python generate_images.py

Images are overwritten in:
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


MODEL_CANDIDATES = ("gpt-image-2", "gpt-image-1")


def generate_image(client: OpenAI, prompt: str, output_path: str) -> bool:
    """Generate an image and save it, trying model fallbacks if needed."""
    print(f"  Generating: {Path(output_path).name}")
    last_error = None
    for model in MODEL_CANDIDATES:
        try:
            response = client.images.generate(
                model=model,
                prompt=prompt,
                size="1024x1024",
            )
            image_bytes = base64.b64decode(response.data[0].b64_json)
            with open(output_path, "wb") as f:
                f.write(image_bytes)
            print(f"    ✓ Saved via {model} ({len(image_bytes) // 1024} KB)")
            return True
        except Exception as exc:
            last_error = exc
            print(f"    ! {model} failed: {exc}")

    print(f"    ✗ All models failed. Last error: {last_error}")
    return False


def main() -> None:
    api_key = ""
    if not api_key:
        raise SystemExit(
            "OPENAI_API_KEY environment variable not set.\n"
            "Set your key and re-run:\n"
            "  Windows PowerShell: $env:OPENAI_API_KEY='sk-...'\n"
            "  python generate_images.py"
        )

    client = OpenAI(api_key=api_key)

    ss_dir = Path("securestar/images")
    hf_dir = Path("harrison-financial/images")
    ss_dir.mkdir(parents=True, exist_ok=True)
    hf_dir.mkdir(parents=True, exist_ok=True)

    images = [
        # SecureStar leadership portraits (company.html team section)
        {
            "file": ss_dir / "priya-nair.png",
            "prompt": (
                "Photorealistic corporate headshot for website leadership profile. "
                "Subject name: Priya Nair, co-founder and CEO of an AI risk infrastructure company. "
                "South Asian woman, late 30s to early 40s, navy blazer, confident approachable expression, "
                "clean neutral studio background, centered framing, chest-up composition, high detail, realistic skin texture."
            ),
        },
        {
            "file": ss_dir / "james-kowalski.png",
            "prompt": (
                "Photorealistic corporate headshot for website leadership profile. "
                "Subject name: James Kowalski, co-founder and CTO. "
                "White man, early 40s, business-casual navy shirt and blazer, focused thoughtful expression, "
                "soft neutral background, chest-up crop, studio lighting, realistic photography."
            ),
        },
        {
            "file": ss_dir / "amara-reeves.png",
            "prompt": (
                "Photorealistic corporate headshot for website leadership profile. "
                "Subject name: Amara Reeves, VP of Engineering. "
                "Black woman, mid-30s, charcoal blazer, confident warm smile, "
                "neutral light background, chest-up framing, sharp focus, realistic professional portrait."
            ),
        },
        {
            "file": ss_dir / "david-marchetti.png",
            "prompt": (
                "Photorealistic corporate headshot for website leadership profile. "
                "Subject name: David Marchetti, Chief Compliance Officer. "
                "White man, mid-50s, dark suit and tie, trustworthy and experienced expression, "
                "neutral studio background, chest-up composition, high realism."
            ),
        },
        {
            "file": ss_dir / "sophia-liu.png",
            "prompt": (
                "Photorealistic corporate headshot for website leadership profile. "
                "Subject name: Sophia Liu, Head of ML Research. "
                "East Asian woman, early 30s, smart blazer, intelligent focused expression, "
                "subtle neutral background, chest-up framing, studio portrait look."
            ),
        },
        {
            "file": ss_dir / "marcus-torres.png",
            "prompt": (
                "Photorealistic corporate headshot for website leadership profile. "
                "Subject name: Marcus Torres, VP of Customer Engineering. "
                "Latino man, late 30s, business-casual shirt and blazer, friendly approachable smile, "
                "neutral background, chest-up crop, realistic studio lighting."
            ),
        },
        # SecureStar customer quote avatars (index.html customer stories)
        {
            "file": ss_dir / "customer-marcus-r.png",
            "prompt": (
                "Photorealistic customer avatar photo for a fintech testimonial card. "
                "Subject label: Marcus R., head of risk engineering persona. "
                "Man in his early 40s, smart-casual attire, friendly professional expression, "
                "close-up headshot, clean background, centered face suitable for circular crop, high realism."
            ),
        },
        {
            "file": ss_dir / "customer-sophia-l.png",
            "prompt": (
                "Photorealistic customer avatar photo for a fintech testimonial card. "
                "Subject label: Sophia L., VP engineering persona. "
                "Woman in late 30s, business-casual attire, confident expression, "
                "close-up headshot, clean background, centered face suitable for circular crop, realistic photo style."
            ),
        },
        {
            "file": ss_dir / "customer-david-p.png",
            "prompt": (
                "Photorealistic customer avatar photo for a fintech testimonial card. "
                "Subject label: David P., chief risk officer persona. "
                "Man in his 50s, business attire, trustworthy expression, "
                "close-up headshot, clean background, centered face suitable for circular crop, natural lighting."
            ),
        },
        # SecureStar office / place (company.html office photo)
        {
            "file": ss_dir / "sf-office.png",
            "prompt": (
                "Photorealistic office environment image for cybersecurity startup company page. "
                "SecureStar headquarters in San Francisco, modern open-plan engineering office, "
                "mix of collaborative tables and standing desks, monitors with analytics dashboards, "
                "glass walls, natural daylight, wide-angle architectural photo, realistic corporate photography."
            ),
        },
        # Harrison Financial leadership portraits (about.html team section)
        {
            "file": hf_dir / "eleanor-harrison.png",
            "prompt": (
                "Photorealistic corporate headshot for digital bank leadership profile. "
                "Subject name: Eleanor Harrison, co-founder and CEO. "
                "White woman, early 40s, elegant navy blazer, confident professional smile, "
                "neutral studio background, chest-up framing, sharp realistic detail."
            ),
        },
        {
            "file": hf_dir / "marcus-reid.png",
            "prompt": (
                "Photorealistic corporate headshot for digital bank leadership profile. "
                "Subject name: Marcus Reid, co-founder and CTO. "
                "Black man, late 30s, dark business shirt and blazer, confident expression, "
                "clean neutral background, chest-up composition, professional studio portrait."
            ),
        },
        {
            "file": hf_dir / "priya-nair.png",
            "prompt": (
                "Photorealistic corporate headshot for digital bank leadership profile. "
                "Subject name: Priya Nair, Chief Risk Officer. "
                "South Asian woman, mid-40s, business blazer with subtle teal accent, "
                "calm and authoritative expression, neutral background, chest-up framing, realistic photo."
            ),
        },
        {
            "file": hf_dir / "james-okafor.png",
            "prompt": (
                "Photorealistic corporate headshot for digital bank leadership profile. "
                "Subject name: James Okafor, Chief Product Officer. "
                "Nigerian man, mid-30s, smart casual blazer, approachable smile, "
                "clean neutral background, chest-up framing, high-quality realistic portrait."
            ),
        },
        {
            "file": hf_dir / "sarah-kwan.png",
            "prompt": (
                "Photorealistic corporate headshot for digital bank leadership profile. "
                "Subject name: Sarah Kwan, General Counsel. "
                "East Asian woman, late 30s, formal dark suit, composed professional expression, "
                "neutral background, chest-up composition, realistic studio lighting."
            ),
        },
        {
            "file": hf_dir / "david-castellano.png",
            "prompt": (
                "Photorealistic corporate headshot for digital bank leadership profile. "
                "Subject name: David Castellano, Chief Financial Officer. "
                "Hispanic man, early 50s, charcoal suit, experienced trustworthy smile, "
                "clean neutral background, chest-up framing, realistic professional portrait."
            ),
        },
        # Harrison Financial member review avatars (index.html testimonials)
        {
            "file": hf_dir / "member-marcus-j.png",
            "prompt": (
                "Photorealistic member avatar for consumer banking testimonial card. "
                "Subject label: Marcus J., everyday banking customer in Chicago. "
                "Man in his 30s, casual modern clothing, genuine smile, "
                "tight headshot, simple background, centered face suitable for circular crop, realistic photo."
            ),
        },
        {
            "file": hf_dir / "member-sarah-r.png",
            "prompt": (
                "Photorealistic member avatar for consumer banking testimonial card. "
                "Subject label: Sarah R., everyday banking customer in Austin. "
                "Woman in her 30s, casual-professional look, friendly expression, "
                "tight headshot, simple background, centered face suitable for circular crop, realistic natural lighting."
            ),
        },
        {
            "file": hf_dir / "member-david-k.png",
            "prompt": (
                "Photorealistic member avatar for consumer banking testimonial card. "
                "Subject label: David K., everyday banking customer in Seattle. "
                "Man in his 40s, casual clothing, approachable expression, "
                "tight headshot, simple background, centered face suitable for circular crop, realistic photography."
            ),
        },
        # Harrison Financial lifestyle / place images (about.html)
        {
            "file": hf_dir / "app-lifestyle.png",
            "prompt": (
                "Photorealistic lifestyle image for a digital bank mission section. "
                "A bank member using a mobile banking app on a smartphone, "
                "modern home environment with natural daylight, candid and optimistic mood, "
                "editorial lifestyle photography, realistic human details."
            ),
        },
        {
            "file": hf_dir / "hf-office.png",
            "prompt": (
                "Photorealistic headquarters image for financial company about page. "
                "Modern fintech office interior, bright and airy with glass meeting rooms, "
                "diverse professionals collaborating at desks with laptops and monitors, "
                "city skyline visible through large windows, wide-angle corporate photo."
            ),
        },
    ]

    print(
        f"Generating {len(images)} images using fallback models "
        f"{', '.join(MODEL_CANDIDATES)}...\n"
    )

    success_count = 0
    failure_count = 0

    print("SecureStar images:")
    securestar_images = [img for img in images if "securestar" in str(img["file"])]
    for img in securestar_images:
        if generate_image(client, img["prompt"], str(img["file"])):
            success_count += 1
        else:
            failure_count += 1
        time.sleep(1)

    print("\nHarrison Financial images:")
    hf_images = [img for img in images if "harrison-financial" in str(img["file"])]
    for img in hf_images:
        if generate_image(client, img["prompt"], str(img["file"])):
            success_count += 1
        else:
            failure_count += 1
        time.sleep(1)

    print(
        f"\nFinished. Success: {success_count}, Failed: {failure_count}. "
        "Output folders: securestar/images/ and harrison-financial/images/"
    )
    if failure_count:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
