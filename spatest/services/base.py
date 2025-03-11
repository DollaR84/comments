import os
import hashlib
from typing import Literal, Optional

from config import Config


class BaseManager:

    def __init__(self, config: Config, filename: str):
        self.config: Config = config
        self.filename: str = filename

        self.name_and_ext = os.path.splitext(self.filename)

    def check_extension(self, allowed_types: list[str]) -> bool:
        return self.name_and_ext[1].upper() in allowed_types if len(self.name_and_ext) > 1 else False

    def get_hash_sum(self, file_mode: Literal["r", "rb"]) -> str:
        file_hash = hashlib.sha256()
        file_encoding: Optional[str] = "utf-8" if file_mode == "r" else None

        with open(self.filename, mode=file_mode, encoding=file_encoding) as data_file:
            content = data_file.read()
            file_hash.update(content)

        return file_hash.hexdigest()
