def generate_story(
    outline,
    story_prompt: str,
    character_name: str,
    tone: str,
):
    """
    Convert the existing comic outline into story panels
    without making another external Gemini API call.
    """

    # Support Pydantic models and dictionaries
    if hasattr(outline, "model_dump"):
        data = outline.model_dump()
    elif isinstance(outline, dict):
        data = outline
    else:
        data = {}

    panels = data.get("panels", [])

    if not panels:
        raise RuntimeError(
            "Gemini outline did not contain any panels."
        )

    story = []

    for index, panel in enumerate(panels, start=1):

        if hasattr(panel, "model_dump"):
            panel = panel.model_dump()
        elif not isinstance(panel, dict):
            panel = {}

        panel_number = panel.get(
            "panel_number",
            index
        )

        title = panel.get(
            "title",
            f"Comic Panel {panel_number}"
        )

        scene_description = panel.get(
            "scene_description",
            ""
        )

        image_prompt = panel.get(
            "image_prompt",
            scene_description
        )

        story.append(
            {
                "panel_number": panel_number,
                "title": title,
                "scene_description": scene_description,
                "image_prompt": image_prompt,
                "caption": panel.get(
                    "caption",
                    scene_description
                ),
                "narration": panel.get(
                    "narration",
                    scene_description
                ),
                "dialogue": panel.get(
                    "dialogue",
                    ""
                ),
            }
        )

    return story