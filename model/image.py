import urllib.request
from PIL import Image as PILImage
import io

class Image():
    data: bytes = None
    width: int = 0
    height: int = 0

    def __init__(self, url):
        try:
            self.data = urllib.request.urlopen(url).read()
            # Get image width and height
            image = PILImage.open(io.BytesIO(self.data))
            self.width, self.height = image.size
        except urllib.error.HTTPError:
            pass