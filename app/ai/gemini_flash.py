from google import genai
from google.genai import types

from app.config import get_settings
from app.models import OutlineResponse


def generate_outline(
    story_prompt: str,
    character_name: str,
    setting: str,
    tone: str,
    art_style: str,
):
    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Add it to your .env file."
        )

    prompt = f"""
Create a coherent {settings.comic_panels}-panel comic outline.

Story idea:
{story_prompt}

Main character:
{character_name}

Setting:
{setting}

Tone:
{tone}

Art style:
{art_style}

Create exactly {settings.comic_panels} panels.

Each panel must contain:

- panel_number
- title
- scene_description
- image_prompt

The image prompt must describe:

- character appearance
- character action
- environment
- composition
- camera framing
- lighting
- mood
- art style

Keep the main character visually consistent throughout all panels.

Do not put dialogue or written text inside the generated image.
"""

    client = genai.Client(
        api_key=settings.gemini_api_key
    )

    response = client.models.generate_content(
        model=settings.gemini_flash_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.9,
            response_mime_type="application/json",
            response_schema=OutlineResponse,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty outline."
        )

    result = OutlineResponse.model_validate_json(
        response.text
    )

    if len(result.panels) != settings.comic_panels:
        raise RuntimeError(
            f"Expected {settings.comic_panels} panels, "
            f"but Gemini returned {len(result.panels)}."
        )

    return [
        panel.model_dump()
        for panel in result.panels
    ]