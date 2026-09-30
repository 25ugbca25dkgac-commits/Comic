from pathlib import Path

from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

from app.config import get_settings
from app.models import PromptRequest

from app.services.gemini_flash import generate_outline
from app.services.gemini_pro import generate_story
from app.services.image_generator import generate_image
from app.services.layout_builder import build_comic_layout
from app.services.exporters import save_pdf


router = APIRouter()

settings = get_settings()

templates = Jinja2Templates(
    directory=str(settings.templates_dir)
)


def run_comic_generation(data: PromptRequest):

    outline = generate_outline(
        story_prompt=data.story_prompt,
        character_name=data.character_name,
        setting=data.setting,
        tone=data.tone,
        art_style=data.art_style,
    )

    story = generate_story(
        outline=outline,
        story_prompt=data.story_prompt,
        character_name=data.character_name,
        tone=data.tone,
    )

    images = []

    for index, panel in enumerate(story, start=1):

        image_prompt = panel.get(
            "image_prompt",
            f"Comic panel {index}: {data.story_prompt}",
        )

        image_path = generate_image(
            prompt=image_prompt,
            panel_number=index,
        )

        images.append(image_path)

    layout = build_comic_layout(
        story_panels=story,
        image_paths=images,
    )

    pdf_url = save_pdf(layout)

    return layout, pdf_url


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "title": "ComicCraft",
            "defaults": {
                "character_name": "",
                "setting": "enchanted forest",
                "tone": "dramatic",
                "art_style": "comic book",
            },
        },
    )


@router.post("/generate", response_class=HTMLResponse)
async def generate(
    request: Request,
    story_prompt: str = Form(...),
    character_name: str = Form(""),
    setting: str = Form("enchanted forest"),
    tone: str = Form("dramatic"),
    art_style: str = Form("comic book"),
):

    data = PromptRequest(
        story_prompt=story_prompt,
        character_name=character_name,
        setting=setting,
        tone=tone,
        art_style=art_style,
    )

    try:

        layout, pdf_url = run_comic_generation(data)

    except Exception as exc:

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            status_code=502,
            context={
                "title": "ComicCraft",
                "error": str(exc),
                "form": data.model_dump(),
            },
        )

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "title": "Your Comic",
            "layout": layout,
            "pdf_url": pdf_url,
        },
    )


@router.post("/generate-comic/json")
async def generate_comic_json(
    data: PromptRequest,
):

    try:

        layout, pdf_url = run_comic_generation(data)

    except Exception as exc:

        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc

    return {
        "message": "Comic generated successfully.",
        "panels": layout,
        "pdf_url": pdf_url,
    }


@router.post("/test-image")
async def test_image(payload: dict):

    prompt = payload.get("prompt")

    if not isinstance(prompt, str) or not prompt.strip():

        raise HTTPException(
            status_code=422,
            detail="A non-empty 'prompt' is required.",
        )

    try:

        image_path = generate_image(
            prompt.strip(),
            0,
        )

        return {
            "image_path": image_path,
        }

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=str(exc),
        ) from exc