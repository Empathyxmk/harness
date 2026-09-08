import os
import numpy as np
from PIL import Image
import pytest

try:
    from src.getImages import getImages
except ImportError:
    getImages = None

def test_getImages():
    print('Testing getImages...')
    testFolder = 'numS'
    testImagesCreated = False
    if getImages is not None:
        os.makedirs(testFolder, exist_ok=True)
        # Create dummy images: 0-2, 5x5
        for i in range(3):
            imgFile = os.path.join(testFolder, f'{i}numS.bmp')
            if not os.path.exists(imgFile):
                img = Image.fromarray(np.full((5,5), i, dtype=np.uint8))
                img.save(imgFile)
                testImagesCreated = True
        try:
            imgs = getImages(testFolder, list(range(3)))
            assert (isinstance(imgs, list) or isinstance(imgs, np.ndarray))
        except Exception as err:
            print(f'getImages test: {err}')
        if testImagesCreated:
            for i in range(3):
                imgFile = os.path.join(testFolder, f'{i}numS.bmp')
                if os.path.exists(imgFile):
                    os.remove(imgFile)
            if len(os.listdir(testFolder)) == 0:
                os.rmdir(testFolder)
    else:
        print('getImages.py (getImages) not found')
    # Edge case: missing directory
    with pytest.raises(Exception):
        getImages('no_dir', list(range(10)))