import logging
from typing import Any

from pydantic import Field
from pydantic_settings import BaseSettings, JsonConfigSettingsSource, SettingsConfigDict


logger = logging.getLogger(__name__)


class BaseConfig(BaseSettings):
    model_config = SettingsConfigDict(json_file="config/config.json", json_file_encoding="utf-8")

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        logger.debug(f"Config initialized: {self.model_dump()}")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: type[BaseSettings],
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (JsonConfigSettingsSource(settings_cls),)


class GameConfig(BaseConfig):
    fps: int = Field(default=60)
    debug: bool = Field(default=False)
