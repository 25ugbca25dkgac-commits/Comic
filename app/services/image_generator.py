from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings


settings = get_settings()


def generate_image(
    prompt: str,
    panel_number: int = 0,
) -> str:

    settings.ensure_directories()

    filename = f"panel_{panel_number}.png"

    output_path = settings.exports_dir / filename

    width = getattr(settings, "image_width", 768)
    height = getattr(settings, "image_height", 512)

    image = Image.new(
        "RGB",
        (width, height),
        "white",
    )

    draw = ImageDraw.Draw(image)

    # Comic panel border
    draw.rectangle(
        [5, 5, width - 5, height - 5],
        outline="black",
        width=6,
    )

    title = f"Comic Panel {panel_number}"

    draw.text(
        (30, 30),
        title,
        fill="black",
    )

    # Wrap prompt
    text = prompt.strip()

    max_chars = 65
    lines = [
        text[i:i + max_chars]
        for i in range(
            0,
            len(text),
            max_chars,
        )
    ]

    y = 100

    for line in lines[:10]:

        draw.text(
            (30, y),
            line,
            fill="black",
        )

        y += 28

    image.save(output_path)

    return str(output_path)