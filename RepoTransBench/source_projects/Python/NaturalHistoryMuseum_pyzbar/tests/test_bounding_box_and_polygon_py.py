import os
import builtins
import sys
import pytest

import bounding_box_and_polygon

def test_file_is_written_and_image_properties(monkeypatch):
    # this actually writes a file, test file existence and remove it
    path = 'bounding_box_and_polygon.png'
    assert os.path.exists(path)
    # Optionally, check PNG header
    with open(path, 'rb') as f:
        magic = f.read(8)
    assert magic == b'\x89PNG\r\n\x1a\n'
    # cleanup
    os.remove(path)

def test_pillow_import(monkeypatch):
    # covers import PIL usage
    import importlib
    PIL = importlib.import_module("PIL")
    assert hasattr(PIL, "Image")
    assert hasattr(PIL, "ImageDraw")