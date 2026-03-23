#!/usr/bin/env python3
"""
使用 gemini-3.1-flash-image 生成 LOD 优化参考图
"""

import requests
import json
import base64
import os
import time
import re

API_URL = "https://aigw.netease.com/v1/chat/completions"
AUTH_TOKEN = "Bearer p4x4nxxigw2ccja7.7vfnst67x7dcmghii83cw47uovjqpmrx"
OUTPUT_DIR = "G:/Trae_ai/netease_aigw/lod_images"
os.makedirs(OUTPUT_DIR, exist_ok=True)

BASE_PROMPT = (
    "As a professional 3D game art textbook illustration. "
    "Style: clay render (gray/white unlit model), visible wireframe mesh topology lines, "
    "clean white background, technical diagram layout. "
    "No overlapping models. Front view. Label poly counts and LOD levels clearly. "
    "Show proper edge flow and topology following anatomy and game industry standards."
)

PROMPTS = [
    {
        "name": "lod0_lod1_high",
        "prompt": (
            BASE_PROMPT +
            "\n\nShow TWO humanoid character gray wireframe models side by side:\n"
            "LEFT - LOD0 (6000 triangles): Full detail mesh. Complete facial topology loops "
            "(eye orbit loops, nasolabial loops). All 5 fingers individually modeled with 4 edge loops each. "
            "Cloth wrinkle details preserved. Proper anatomical edge flow.\n"
            "RIGHT - LOD1 (4000 triangles): First optimization pass. Remove interior edge loops on flat surfaces. "
            "Merge coplanar faces. Keep silhouette vertices. Fingers still separated but reduced to 2 loops each.\n"
            "Label below each: 'LOD0 - 6000 tris' and 'LOD1 - 4000 tris'. "
            "Add annotation arrows showing 'Remove interior edge loops' and 'Merge coplanar quads'."
        ),
    },
    {
        "name": "lod2_lod3_mid",
        "prompt": (
            BASE_PROMPT +
            "\n\nShow TWO humanoid character gray wireframe models side by side:\n"
            "LEFT - LOD2 (2500 triangles): Medium optimization. Hands simplified to mitten shape (no individual fingers). "
            "Facial topology reduced to basic form. Joint edge loops preserved for animation. "
            "Torso uses large merged quads.\n"
            "RIGHT - LOD3 (1200 triangles): Medium-low. Limb cross-section reduced from octagon to hexagon. "
            "Ear inner structure removed. All cloth folds flattened. Face keeps only eye socket depression and nose bridge.\n"
            "Label below each: 'LOD2 - 2500 tris' and 'LOD3 - 1200 tris'. "
            "Annotations: 'Mitten hands', 'Hexagonal limb section', 'Remove ear cavity'."
        ),
    },
    {
        "name": "lod4_lod5_low",
        "prompt": (
            BASE_PROMPT +
            "\n\nShow TWO humanoid character gray wireframe models side by side:\n"
            "LEFT - LOD4 (600 triangles): Low poly. Limbs are square cross-section tubes. "
            "Head is basic sphere. Hands merged into single wedge block. No facial features. "
            "Single edge loop at each joint.\n"
            "RIGHT - LOD5 (350 triangles): Very low poly. Torso is a single box shape. "
            "Legs are simple cones. Arms are cylinders. Head is 8-sided sphere.\n"
            "Label below each: 'LOD4 - 600 tris' and 'LOD5 - 350 tris'. "
            "Annotations: 'Box torso', 'Cone legs', 'Wedge hands'."
        ),
    },
    {
        "name": "lod6_and_overview",
        "prompt": (
            BASE_PROMPT +
            "\n\nTOP HALF - LOD6 (200 triangles): Absolute minimum. Entire body built from geometric primitives. "
            "Head is 6-face low-poly sphere. Torso is rectangular box. Each limb is 4-6 triangles cone/cylinder. "
            "No fingers, no face, no joints. Label: 'LOD6 - 200 tris - Geometric primitives only'.\n"
            "BOTTOM HALF - Complete LOD chain comparison strip showing 7 small figures left to right:\n"
            "LOD0(6000) - LOD1(4000) - LOD2(2500) - LOD3(1200) - LOD4(600) - LOD5(350) - LOD6(200)\n"
            "Each figure gets progressively simpler. All gray wireframe clay render. "
            "Title: 'Complete LOD Chain - Game Character Optimization Pipeline'."
        ),
    },
]


def generate_image(prompt_data, index):
    """Generate one LOD image."""
    print(f"\n{'='*60}")
    print(f"[{index+1}/4] Generating: {prompt_data['name']}")
    print(f"{'='*60}")

    for attempt in range(3):
        try:
            resp = requests.post(
                API_URL,
                headers={
                    "Authorization": AUTH_TOKEN,
                    "Content-Type": "application/json",
                },
                json={
                    "model": "gemini-3.1-flash-image",
                    "messages": [{"role": "user", "content": prompt_data["prompt"]}],
                    "max_tokens": 8192,
                    "temperature": 0.8,
                    "vertexai": {
                        "response_modalities": ["IMAGE", "TEXT"],
                    },
                },
                timeout=180,
            )

            if resp.status_code == 429:
                wait = 30 * (attempt + 1)
                print(f"  Rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue

            data = resp.json()

            if "error" in data:
                print(f"  API error: {data['error']['message'][:200]}")
                if attempt < 2:
                    time.sleep(15)
                    continue
                return False

            msg = data["choices"][0]["message"]
            content = msg.get("content", "")
            usage = data.get("usage", {})
            print(f"  Tokens: prompt={usage.get('prompt_tokens')}, "
                  f"completion={usage.get('completion_tokens')}, "
                  f"total={usage.get('total_tokens')}")

            saved = _try_save_image(content, prompt_data["name"])

            if not saved:
                # Save raw JSON for debug
                raw_path = os.path.join(OUTPUT_DIR, f"{prompt_data['name']}_raw.json")
                with open(raw_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                print(f"  No image extracted. Raw response -> {raw_path}")
                preview = str(content)
                print(f"  Content preview ({len(preview)} chars): {preview[:400]}")

            return True

        except requests.exceptions.Timeout:
            print(f"  Timeout (attempt {attempt+1}/3)")
            if attempt < 2:
                time.sleep(10)
        except Exception as e:
            print(f"  Exception: {e}")
            if attempt < 2:
                time.sleep(10)

    return False


def _try_save_image(content, name):
    """Try to extract and save base64 image from content."""
    if not isinstance(content, str):
        return False

    # Pattern: data:image/xxx;base64,DATA
    m = re.findall(r"data:image/(png|jpeg|jpg|webp);base64,([A-Za-z0-9+/=]+)", content)
    if m:
        ext = "png" if m[0][0] == "png" else "jpg"
        path = os.path.join(OUTPUT_DIR, f"{name}.{ext}")
        with open(path, "wb") as f:
            f.write(base64.b64decode(m[0][1]))
        print(f"  Saved: {path} ({os.path.getsize(path):,} bytes)")
        return True

    # Pattern: raw base64 blob (PNG / JPEG header)
    m = re.findall(r"(iVBOR[A-Za-z0-9+/=\n]{100,}|/9j/[A-Za-z0-9+/=\n]{100,})", content)
    if m:
        blob = m[0].replace("\n", "")
        ext = "png" if blob.startswith("iVBOR") else "jpg"
        path = os.path.join(OUTPUT_DIR, f"{name}.{ext}")
        with open(path, "wb") as f:
            f.write(base64.b64decode(blob))
        print(f"  Saved: {path} ({os.path.getsize(path):,} bytes)")
        return True

    return False


if __name__ == "__main__":
    for i, p in enumerate(PROMPTS):
        generate_image(p, i)
        if i < len(PROMPTS) - 1:
            print("\nCooling down 20s ...")
            time.sleep(20)

    print(f"\n{'='*60}")
    print(f"Output directory: {OUTPUT_DIR}")
    print(f"{'='*60}")
    if os.path.isdir(OUTPUT_DIR):
        for f in sorted(os.listdir(OUTPUT_DIR)):
            sz = os.path.getsize(os.path.join(OUTPUT_DIR, f))
            print(f"  {f}  ({sz:,} bytes)")
