import numpy as np
import pytest
from src.hyeonwoonoh_deconvnet.inference.util.preprocess_image import preprocess_image

class TestPreprocessImage:
    def test_basic_functionality(self):
        img = (np.random.rand(300, 400, 3) * 255).astype(np.uint8)
        img_sz = 500
        preprocessed = preprocess_image(img, img_sz)
        assert isinstance(preprocessed, list)
        assert len(preprocessed) == 1
        pre_img = preprocessed[0]
        assert pre_img.dtype == np.float32
        assert pre_img.shape == (img_sz, img_sz, 3)
        assert pre_img.min() > -200
        assert pre_img.max() < 200

    def test_edgecase_square_image(self):
        img = (np.random.rand(200, 200, 3) * 255).astype(np.uint8)
        img_sz = 224
        preprocessed = preprocess_image(img, img_sz)
        pre_img = preprocessed[0]
        assert pre_img.shape == (img_sz, img_sz, 3)

    def test_edgecase_single_pixel_image(self):
        img = (np.random.rand(1, 1, 3) * 255).astype(np.uint8)
        img_sz = 100
        preprocessed = preprocess_image(img, img_sz)
        pre_img = preprocessed[0]
        assert pre_img.shape == (img_sz, img_sz, 3)