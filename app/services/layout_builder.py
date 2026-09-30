from pathlib import Path


def build_comic_layout(
    story_panels: list,
    image_paths: list,
) -> list:

    layout = []

    for index, panel in enumerate(story_panels):

        image_path = ""

        if index < len(image_paths):
            image_path = str(image_paths[index])

        layout.append(
            {
                "panel_number": panel.get(
                    "panel_number",
                    index + 1,
                ),
                "title": panel.get(
                    "title",
                    f"Panel {index + 1}",
                ),
                "scene_description": panel.get(
                    "scene_description",
                    "",
                ),
                "caption": panel.get(
                    "caption",
                    "",
                ),
                "narration": panel.get(
                    "narration",
                    "",
                ),
                "dialogue": panel.get(
                    "dialogue",
                    "",
                ),
                "image_prompt": panel.get(
                    "image_prompt",
                    "",
                ),
                "image_path": image_path,
            }
        )

    return layout