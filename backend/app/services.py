import asyncio
import json
import os
import random
import time
import uuid
from pathlib import Path
from urllib.parse import quote, urlencode

import httpx

from .fallback import fallback_reality
from .prompts import build_image_prompts, build_reality_prompt


BASE_DIRECTORY = Path(__file__).resolve().parent.parent
GENERATED_IMAGES_DIRECTORY = BASE_DIRECTORY / "generated-images"
GEMINI_API_BASE = "https://generativelanguage.googleapis.com/v1beta"

REQUIRED_KEYS = (
    "realityName",
    "divergencePoint",
    "summary",
    "narration",
    "probability",
    "timeline",
    "keyEvents",
    "alternateSelf",
    "worldChanges",
    "longTermConsequences",
    "visualScenes",
)

REALITY_SCHEMA = {
    "type": "object",
    "properties": {
        "realityName": {"type": "string"},
        "divergencePoint": {"type": "string"},
        "summary": {"type": "string"},
        "narration": {"type": "string"},
        "probability": {"type": "string"},
        "timeline": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "year": {"type": "string"},
                    "event": {"type": "string"},
                },
                "required": ["year", "event"],
            },
        },
        "keyEvents": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title", "description"],
            },
        },
        "alternateSelf": {
            "type": "object",
            "properties": {
                "role": {"type": "string"},
                "location": {"type": "string"},
                "relationships": {"type": "string"},
                "innerConflict": {"type": "string"},
            },
            "required": ["role", "location", "relationships", "innerConflict"],
        },
        "worldChanges": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title", "description"],
            },
        },
        "longTermConsequences": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                },
                "required": ["title", "description"],
            },
        },
        "visualScenes": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3,
        },
    },
    "required": list(REQUIRED_KEYS),
}


async def generate_with_gemini(prompt: str):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"{GEMINI_API_BASE}/models/{model}:generateContent"
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": build_reality_prompt(prompt)}]}
        ],
        "generationConfig": {
            "temperature": 1.0,
            "topP": 0.95,
            "maxOutputTokens": 6144,
            "responseMimeType": "application/json",
            "responseSchema": REALITY_SCHEMA,
        },
    }

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            url,
            headers={"x-goog-api-key": api_key},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    response_text = "".join(part.get("text", "") for part in parts)
    if not response_text:
        raise RuntimeError("Gemini returned an empty reality.")

    return json.loads(response_text)


def word_count(text: str) -> int:
    return len(str(text or "").split())


async def rewrite_narration_to_target_length(reality: dict, prompt: str):
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        return None

    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    url = f"{GEMINI_API_BASE}/models/{model}:generateContent"
    rewrite_prompt = f"""
Rewrite only the narration for this PARACOSM result.

Exact user question:
{prompt}

Reality name:
{reality.get('realityName', '')}

Divergence point:
{reality.get('divergencePoint', '')}

Summary:
{reality.get('summary', '')}

Current narration:
{reality.get('narration', '')}

Rules:
- Return only the rewritten narration text. No JSON.
- The narration must be 300 to 500 words. Aim for 380 to 450 words.
- Use simple, natural, human language.
- Use 6 to 8 paragraphs with blank lines between paragraphs.
- Keep the same reality facts, but expand the events step by step.
- Do not add headings, bullet points, labels, or screenplay formatting.
"""
    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": rewrite_prompt}]}
        ],
        "generationConfig": {
            "temperature": 0.9,
            "topP": 0.95,
            "maxOutputTokens": 4096,
        },
    }

    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(
            url,
            headers={"x-goog-api-key": api_key},
            json=payload,
        )
        response.raise_for_status()
        data = response.json()

    parts = data.get("candidates", [{}])[0].get("content", {}).get("parts", [])
    rewritten = "".join(part.get("text", "") for part in parts).strip()
    return rewritten or None


async def enforce_narration_length(reality: dict, prompt: str) -> dict:
    current_words = word_count(reality.get("narration", ""))
    if 300 <= current_words <= 500:
        return reality

    try:
        rewritten = await rewrite_narration_to_target_length(reality, prompt)
    except Exception as error:
        print(f"Gemini narration rewrite failed: {error}")
        return reality

    if rewritten and 300 <= word_count(rewritten) <= 500:
        reality["narration"] = rewritten
    elif rewritten and current_words < 300:
        reality["narration"] = rewritten

    return reality


def normalize_reality(generated, prompt: str) -> dict:
    fallback = fallback_reality(prompt)
    if not isinstance(generated, dict):
        return fallback

    result = {**fallback, **generated}
    for key in REQUIRED_KEYS:
        if result.get(key) is None:
            result[key] = fallback[key]

    for key in (
        "timeline",
        "keyEvents",
        "worldChanges",
        "longTermConsequences",
        "visualScenes",
    ):
        if not isinstance(result[key], list):
            result[key] = fallback[key]

    if not isinstance(result["alternateSelf"], dict):
        result["alternateSelf"] = fallback["alternateSelf"]
    else:
        result["alternateSelf"] = {
            **fallback["alternateSelf"],
            **result["alternateSelf"],
        }

    return result


def fallback_image_url(prompt: str, index: int) -> str:
    title = quote(f"PARACOSM {index + 1}")
    description = quote(prompt[:96])
    return (
        "https://placehold.co/1280x720/111719/f7ead8"
        f"?text={title}%0A{description}"
    )


def image_extension(content_type: str) -> str:
    if "png" in content_type:
        return "png"
    if "webp" in content_type:
        return "webp"
    return "jpg"


async def _try_pollinations(client, base_url, safe_prompt, params, api_key):
    """One attempt against Pollinations. Returns image bytes + content-type, or raises."""
    url = f"{base_url}/prompt/{quote(safe_prompt, safe='')}?{urlencode(params)}"
    # Token goes in the Authorization header only. Passing it as a query param
    # trips Pollinations' "query parameter validation".
    headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}

    response = await client.get(url, headers=headers)
    if response.status_code >= 400:
        body = (response.text or "")[:180].replace("\n", " ")
        raise RuntimeError(f"HTTP {response.status_code}: {body}")

    content_type = response.headers.get("content-type", "image/jpeg")
    if not content_type.startswith("image/"):
        raise RuntimeError(f"non-image response: {(response.text or '')[:120]}")
    return response.content, content_type


async def generate_pollinations_image(prompt: str, index: int, public_url: str) -> str:
    api_key = os.getenv("POLLINATIONS_API_KEY", "").strip()
    base_url = os.getenv("POLLINATIONS_BASE_URL", "https://image.pollinations.ai")
    model = os.getenv("POLLINATIONS_MODEL", "flux")
    # Seed must be a small positive integer. time.time()*1000 (~1.7 trillion)
    # overflows Pollinations' allowed range and fails query validation.
    seed = random.randint(0, 1_000_000_000)
    safe_prompt = prompt[:300]

    base = {"width": 1280, "height": 720, "seed": seed}

    # Fallback ladder: the first that returns an image wins. The richer options
    # (nologo/private) need a paid Pollinations tier and 500 on free tokens, so
    # we degrade toward a bare anonymous request.
    strategies = [
        {**base, "model": model, "nologo": "true"},
        {**base, "model": model},
        {**base, "model": "turbo"},
        {**base},
    ]

    attempts = int(os.getenv("POLLINATIONS_MAX_ATTEMPTS", "2"))
    async with httpx.AsyncClient(timeout=180, follow_redirects=True) as client:
        for params in strategies:
            label = params.get("model", "default")
            for attempt in range(1, attempts + 1):
                try:
                    content, content_type = await _try_pollinations(
                        client, base_url, safe_prompt, params, api_key
                    )
                    GENERATED_IMAGES_DIRECTORY.mkdir(parents=True, exist_ok=True)
                    filename = f"{int(time.time() * 1000)}-{uuid.uuid4()}.{image_extension(content_type)}"
                    (GENERATED_IMAGES_DIRECTORY / filename).write_bytes(content)
                    return f"{public_url}/generated/{filename}"
                except Exception as error:
                    print(
                        f"Pollinations image {index + 1} [{label}] "
                        f"attempt {attempt}/{attempts} failed: {error}"
                    )
                    await asyncio.sleep(1.5 * attempt)

    print(f"Pollinations image {index + 1}: all strategies failed, using placeholder.")
    return fallback_image_url(prompt, index)


async def generate_images(image_prompts, public_url: str):
    count = int(os.getenv("IMAGE_COUNT", "3"))
    prompts = image_prompts[:count]
    api_key = os.getenv("POLLINATIONS_API_KEY", "").strip()

    if not api_key:
        return [
            fallback_image_url(prompt, index)
            for index, prompt in enumerate(prompts)
        ]

    delay = float(os.getenv("POLLINATIONS_REQUEST_DELAY_SECONDS", "5.2"))
    images = []
    for index, prompt in enumerate(prompts):
        if index:
            await asyncio.sleep(delay)
        images.append(await generate_pollinations_image(prompt, index, public_url))
    return images


async def generate_alternate_reality(prompt: str, public_url: str) -> dict:
    generated = await generate_with_gemini(prompt)
    reality = normalize_reality(generated, prompt)
    reality = await enforce_narration_length(reality, prompt)
    image_prompts = build_image_prompts(reality, prompt)
    images = await generate_images(image_prompts, public_url)

    return {
        "reality": reality,
        "imagePrompts": image_prompts,
        "images": images,
    }
