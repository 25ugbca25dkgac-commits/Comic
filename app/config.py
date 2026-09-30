from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )

    app_name: str = "ComicCraft"

    # Gemini
    gemini_api_key: str = ""
    gemini_flash_model: str = "gemini-2.5-flash"
    gemini_pro_model: str = "gemini-2.5-pro"

    # Hugging Face
    hf_token: str = ""
    hf_provider: str = "auto"

    # Image generation
    image_backend: str = "huggingface"
    image_model_id: str = "runwayml/stable-diffusion-v1-5"

    # Local Diffusers
    diffusers_device: str = "auto"

    # Image configuration
    image_width: int = 768
    image_height: int = 512
    image_steps: int = 25
    image_guidance_scale: float = 7.5

    # Comic
    comic_panels: int = 5
    max_prompt_length: int = 2000

    # Directories
    templates_dir: Path = BASE_DIR / "templates"
    static_dir: Path = BASE_DIR / "static"

    panels_dir: Path = BASE_DIR / "static" / "panels"
    exports_dir: Path = BASE_DIR / "static" / "exports"

    def ensure_directories(self):
        self.panels_dir.mkdir(
            parents=True,
            exist_ok=True,
        )

        self.exports_dir.mkdir(
            parents=True,
            exist_ok=True,
        )


@lru_cache
def get_settings() -> Settings:
    settings = Settings()

    settings.ensure_directories()

    return settings