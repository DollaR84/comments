import os

from .base import BaseManager
from .types import FileType


class TextManager(BaseManager):

    @property
    def allowed_type(self) -> bool:
        return self.check_extension(self.config.text.types)

    @property
    def hash_sum(self) -> str:
        return self.get_hash_sum(FileType.text)

    def check_max_size(self) -> bool:
        size = os.stat(self.filename).st_size
        return size <= self.config.text.max_size

    def save(self) -> str:
        file_path = self.get_file_path(FileType.text)
        with open(self.filename, "r", encoding="utf-8") as upload_file:
            with open(file_path, "w", encoding="utf-8") as data_file:
                data_file.write(upload_file.read())
        return file_path
