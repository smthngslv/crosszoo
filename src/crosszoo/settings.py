from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

__all__ = ("Settings",)


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="CROSSZOO_", env_file=".env")

    BOT_TOKEN: str = Field()
    MUTE: bool = Field(default=False)
    WARNINGS: int = Field(default=3)
    BOT_ALIASES_TO_ALLOW: str = Field(
        default="pic,gif,locplacebot,textutilsbot,kozrandbot,lybot,vkmusic_bot,jigsawpuzzlebot"
    )
