from PIL import Image

from .base import BaseManager


class MediaManager(BaseManager):

    @property
    def allowed_type(self) -> bool:
        return self.check_extension(self.config.media.types)

    def check_sizes(self, image: Image) -> bool:
        try:
            width: int
            height: int
            width, height = image.size
        except (AttributeError, TypeError):
            return False
        else:
            return width <= self.config.media.max_width and height <= self.config.media.max_height

    def resize(self, image: Image) -> Image:
        image.thumbnail((self.config.media.max_width, self.config.media.max_height))
        return image

    def save_image(self) -> None:
        with Image.open(self.filename) as image:
            if not self.check_sizes(image):
                image = self.resize(image)
            image.save(self.filename)
