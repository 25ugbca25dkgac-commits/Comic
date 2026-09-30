from pathlib import Path
from datetime import datetime

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.config import get_settings


settings = get_settings()


def save_pdf(layout: list) -> str:

    settings.ensure_directories()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"comic_{timestamp}.pdf"

    output_path = settings.exports_dir / filename

    pdf = canvas.Canvas(
        str(output_path),
        pagesize=A4,
    )

    width, height = A4

    for panel in layout:

        pdf.setFont(
            "Helvetica-Bold",
            18,
        )

        pdf.drawString(
            40,
            height - 50,
            panel.get(
                "title",
                "Comic Panel",
            ),
        )

        pdf.setFont(
            "Helvetica",
            11,
        )

        y = height - 90

        fields = [
            (
                "Scene",
                panel.get(
                    "scene_description",
                    "",
                ),
            ),
            (
                "Caption",
                panel.get(
                    "caption",
                    "",
                ),
            ),
            (
                "Narration",
                panel.get(
                    "narration",
                    "",
                ),
            ),
            (
                "Dialogue",
                panel.get(
                    "dialogue",
                    "",
                ),
            ),
        ]

        for label, value in fields:

            pdf.setFont(
                "Helvetica-Bold",
                11,
            )

            pdf.drawString(
                40,
                y,
                f"{label}:",
            )

            y -= 18

            pdf.setFont(
                "Helvetica",
                10,
            )

            text = str(value)

            for i in range(
                0,
                len(text),
                90,
            ):

                pdf.drawString(
                    55,
                    y,
                    text[i:i + 90],
                )

                y -= 15

            y -= 10

        image_path = panel.get(
            "image_path"
        )

        if image_path:

            image_file = Path(
                image_path
            )

            if image_file.exists():

                try:

                    pdf.drawImage(
                        str(image_file),
                        40,
                        60,
                        width=520,
                        height=250,
                        preserveAspectRatio=True,
                        anchor="c",
                    )

                except Exception:
                    pass

        pdf.showPage()

    pdf.save()

    return f"/download/{filename}"