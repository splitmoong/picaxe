#ImageItem.py

from pathlib import Path
from PIL import Image

class ImageItem:
    def __init__(self, path: Path):
        self.path = path
        self.original_size = path.stat().st_size
        self.original_type = path.suffix[1:].lower()
        self.target_type = None
        self.target_size = None
        self.quality = None
        self.metadata = self.load_metadata()

    #loading and storing metadata in a dict
    def load_metadata(self):
        metadata = {}
        img = Image.open(self.path)

        #jpg has exif
        if hasattr(img, "_getexif"):
            exif_data = img._getexif()
            if exif_data:
                metadata.update(exif_data)

        #png or others
        metadata.update(img.info)
        return metadata

    #function to strip metadata
    def strip_metadata(self, output_path: Path):
        img = Image.open(self.path)
        data = list(img.getdata())
        new_img = Image.new(img.mode, img.size)
        new_img.putdata(data)
        new_img.save(output_path)

    @property
    def size_kb(self):
        #returns size in kb
        return self.original_size / 1024

    def __repr__(self):
        return f"<ImageItem path={self.path} type={self.original_type} size={self.size_kb:.1f}KB>"