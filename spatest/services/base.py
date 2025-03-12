from abc import ABC, abstractmethod
import os
import hashlib
import pathlib
from typing import Literal, Optional

from config import Config

from .types import FileType


class BaseManager(ABC):

    def __init__(self, config: Config, filename: str):
        self.config: Config = config
        self.filename: str = filename

        self.name_and_ext = os.path.splitext(self.filename)

    def check_extension(self, allowed_types: list[str]) -> bool:
        return self.name_and_ext[1].upper() in allowed_types if len(self.name_and_ext) > 1 else False

    def get_hash_sum(self, file_type: FileType) -> str:
        file_hash = hashlib.sha256()
        file_mode: Literal["r", "rb"] = "rb" if file_type == FileType.image else "r"
        file_encoding: Optional[str] = "utf-8" if file_type == FileType.text else None

        with open(self.filename, mode=file_mode, encoding=file_encoding) as data_file:
            content = data_file.read()
            file_hash.update(content)

        return file_hash.hexdigest()

    def get_file_path(self, file_type: FileType) -> str:
        subfolder = "images" if file_type == FileType.image else "texts"
        filename = os.path.basename(self.filename)
        return str(pathlib.Path(self.filename).parents[2] / subfolder / filename)

    @abstractmethod
    def save(self) -> str:
        raise NotImplementedError

    def delete_upload_file(self) -> None:
        try:
            os.remove(self.filename)
        except Exception:
            pass
