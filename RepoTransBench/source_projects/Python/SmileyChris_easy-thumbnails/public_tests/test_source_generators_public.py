import pytest
from easy_thumbnails.source_generators import pil_image_source

def test_pil_image_source_tuple_public():
    from PIL import Image
    img = Image.new('RGBA', (4, 4), (50, 100, 150, 202))
    img.format = "PNG"
    src = pil_image_source(img)
    assert src.size == (4, 4)
    assert img.format == "PNG"

def test_pil_image_source_bytes_public():
    from PIL import Image
    import io
    img = Image.new('RGB', (2, 2), (91, 42, 99))
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    loaded = pil_image_source(buf)
    assert loaded.size == (2, 2)

def test_pil_image_source_str_path_public(tmp_path):
    # Provide a unique test file path
    from PIL import Image
    import os
    file_path = tmp_path / "sample_public_image.png"
    img = Image.new("L", (3, 3))
    img.save(file_path)
    loaded = pil_image_source(str(file_path))
    assert loaded.size == (3, 3)