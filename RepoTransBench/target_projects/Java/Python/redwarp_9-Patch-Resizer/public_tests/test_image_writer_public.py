import os
import tempfile
import shutil
from PIL import Image
import enum

class Output(enum.Enum):
    PNG = "png"
    JPG = "jpg"

class ImageWriter:
    @staticmethod
    def write(img, out_type, filename):
        if img is None or out_type is None or filename is None:
            return
        img.save(filename, out_type.value.upper())

    @staticmethod
    def copy(input_fp, output_fp):
        if input_fp is None or output_fp is None:
            return
        with open(input_fp, "rb") as fsrc, open(output_fp, "wb") as fdst:
            shutil.copyfileobj(fsrc, fdst)

class TestImageWriterPublic:
    def setup_method(self):
        self.img = Image.new("RGB", (15, 8))
        draw = self.img.load()
        for x in range(1, 14):
            for y in range(1, 7):
                draw[x, y] = (50, 120, 200)
        for x in range(15):
            for y in range(8):
                if x == 0 or y == 0 or x == 14 or y == 7:
                    draw[x, y] = (0, 0, 0)
        self.output_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self.output_file.close()
        self.input_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        self.input_file.close()
        self.img.save(self.input_file.name, "PNG")

    def teardown_method(self):
        if os.path.exists(self.output_file.name):
            os.remove(self.output_file.name)
        if os.path.exists(self.input_file.name):
            os.remove(self.input_file.name)

    def test_write_png(self):
        ImageWriter.write(self.img, Output.PNG, self.output_file.name)
        assert os.path.exists(self.output_file.name)
        loaded = Image.open(self.output_file.name)
        assert loaded is not None
        assert loaded.size == self.img.size

    def test_write_jpg(self):
        jpg_output = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
        jpg_output.close()
        try:
            ImageWriter.write(self.img, Output.JPG, jpg_output.name)
            assert os.path.exists(jpg_output.name)
            loaded = Image.open(jpg_output.name)
            assert loaded is not None
            assert loaded.size == self.img.size
        finally:
            if os.path.exists(jpg_output.name):
                os.remove(jpg_output.name)

    def test_copy(self):
        copy_file = tempfile.NamedTemporaryFile(delete=False, suffix=".png")
        copy_file.close()
        try:
            ImageWriter.copy(self.input_file.name, copy_file.name)
            assert os.path.exists(copy_file.name)
            loaded = Image.open(copy_file.name)
            assert loaded is not None
        finally:
            if os.path.exists(copy_file.name):
                os.remove(copy_file.name)

    def test_copy_null_inputs(self):
        ImageWriter.copy(None, None)  # Should not raise