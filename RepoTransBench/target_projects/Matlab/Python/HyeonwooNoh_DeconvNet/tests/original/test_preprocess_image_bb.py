import numpy as np
import pytest
from src.hyeonwoonoh_deconvnet.inference.util.preprocess_image_bb import preprocess_image_bb

class TestPreprocessImageBB:
    def test_basic_functionality(self):
        img = (np.random.rand(300, 400, 3) * 255).astype(np.uint8)
        box = [50, 60, 250, 300]
        img_sz = 224
        preprocessed = preprocess_image_bb(img, box, img_sz)
        assert isinstance(preprocessed, list)
        assert len(preprocessed) == 1
        pre_img = preprocessed[0]
        assert pre_img.dtype == np.float32
        assert pre_img.shape == (img_sz, img_sz, 3)
        assert pre_img.min() > -200
        assert pre_img.max() < 200

    def test_edgecase_small_box(self):
        img = (np.random.rand(100, 100, 3) * 255).astype(np.uint8)
        box = [1, 1, 10, 10]
        img_sz = 224
        preprocessed = preprocess_image_bb(img, box, img_sz)
        pre_img = preprocessed[0]
        assert pre_img.shape == (img_sz, img_sz, 3)

    def test_edgecase_image_equal_to_box(self):
        img = (np.random.rand(200, 200, 3) * 255).astype(np.uint8)
        box = [1, 1, 200, 200]
        img_sz = 224
        preprocessed = preprocess_image_bb(img, box, img_sz)
        pre_img = preprocessed[0]
        assert pre_img.shape == (img_sz, img_sz, 3)

    def test_edgecase_single_pixel_box(self):
        img = (np.random.rand(10, 10, 3) * 255).astype(np.uint8)
        box = [5, 5, 5, 5]
        img_sz = 224
        preprocessed = preprocess_image_bb(img, box, img_sz)
        pre_img = preprocessed[0]
        assert pre_img.shape == (img_sz, img_sz, 3)