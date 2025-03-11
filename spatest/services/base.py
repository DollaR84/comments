import os

from config import Config


class BaseManager:

    def __init__(self, config: Config, filename: str):
        self.config: Config = config
        self.filename: str = filename

    def check_extension(self, allowed_types: list[str]) -> bool:
        name_and_ext = os.path.splitext(self.filename)
        return name_and_ext[1].upper() in allowed_types if len(name_and_ext) > 1 else False
