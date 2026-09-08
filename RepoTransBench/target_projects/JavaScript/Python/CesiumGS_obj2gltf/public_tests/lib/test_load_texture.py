import pytest
import sys
import os

# Adjust sys.path so that src/loadTexture.py can be imported, regardless of test runner location
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..", "src")))
import loadTexture

altPngTexturePath = "specs/data/box-texture-options/bump.png"
altJpgTexturePath = "specs/data/box-complex-material-alpha/emission.jpg"
altJpegTexturePath = "specs/data/box-complex-material-alpha/specular.jpeg"
altGifTexturePath = "specs/data/box-texture-options/ambient.gif"
altGrayscaleTexturePath = "specs/data/box-complex-material-alpha/alpha.png"
altTransparentTexturePath = "specs/data/box-complex-material-alpha/diffuse.png"

@pytest.mark.asyncio
@pytest.mark.parametrize("texture_path,expect_transparent,expect_name,expect_extension", [
    (altPngTexturePath, False, "bump", ".png"),
    (altJpgTexturePath, False, "emission", ".jpg"),
    (altJpegTexturePath, False, "specular", ".jpeg"),
    (altGifTexturePath, False, "ambient", ".gif"),
    (altGrayscaleTexturePath, True, "alpha", ".png"),
    (altTransparentTexturePath, True, "diffuse", ".png"),
])
async def test_load_texture(texture_path, expect_transparent, expect_name, expect_extension):
    # The stub is sync, so mimic async call manually
    # Use "await" in the future for truly async `loadTexture`
    texture = loadTexture.loadTexture(texture_path)
    assert texture.transparent == expect_transparent
    assert texture.source is not None
    assert texture.name == expect_name
    assert texture.extension == expect_extension
    assert texture.path == texture_path
    assert texture.pixels is None
    assert texture.width is None
    assert texture.height is None