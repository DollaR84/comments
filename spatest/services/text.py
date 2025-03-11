import os

from .base import BaseManager


class TextManager(BaseManager):

    @property
    def allowed_type(self) -> bool:
        return self.check_extension(self.config.text.types)

    def check_max_size(self) -> bool:
        size = os.stat(self.filename).st_size
        return size <= self.config.text.max_size
