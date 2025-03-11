from dataclasses import dataclass, field


@dataclass(slots=True)
class MediaConfig:
    max_width: int = 320
    max_height: int = 240
    types: list[str] = [".JPG", ".GIF", ".PNG"]


@dataclass(slots=True)
class TextConfig:
    max_size: int = 100 * 1024
    types: list[str] = [".TXT"]


@dataclass(slots=True)
class Config:
    media: MediaConfig = field(default_factory=MediaConfig)
    text: TextConfig = field(default_factory=TextConfig)
