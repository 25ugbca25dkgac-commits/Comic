from pydantic import BaseModel, Field, field_validator


class PromptRequest(BaseModel):
    story_prompt: str = Field(
        ...,
        min_length=3,
        max_length=2000,
    )

    character_name: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    setting: str = Field(
        ...,
        min_length=1,
        max_length=120,
    )

    tone: str = Field(
        ...,
        min_length=1,
        max_length=60,
    )

    art_style: str = Field(
        ...,
        min_length=1,
        max_length=80,
    )

    @field_validator(
        "story_prompt",
        "character_name",
        "setting",
        "tone",
        "art_style",
        mode="before",
    )
    @classmethod
    def strip_values(cls, value):

        if isinstance(value, str):
            return value.strip()

        return value


class PanelOutline(BaseModel):
    panel_number: int = Field(..., ge=1)

    title: str

    scene_description: str

    image_prompt: str


class OutlineResponse(BaseModel):
    panels: list[PanelOutline] = Field(
        min_length=1
    )


class PanelStory(BaseModel):
    panel_number: int = Field(..., ge=1)

    title: str

    scene_description: str

    caption: str

    narration: str

    dialogue: str

    image_prompt: str


class StoryResponse(BaseModel):
    panels: list[PanelStory] = Field(
        min_length=1
    )


class ComicPanel(BaseModel):
    panel_number: int

    title: str

    image_path: str

    scene_description: str

    caption: str

    narration: str

    dialogue: str

    image_prompt: str