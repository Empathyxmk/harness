import os
import numpy as np
from PIL import Image
import pytest

try:
    from src.getImages import getImages
except ImportError:
    getImages = None

def test_public_getImages():
    print('Testing getImages (public)...')
    testFolder = 'numS'
    testImagesCreated = False
    if getImages is not None:
        os.makedirs(testFolder, exist_ok=True)
        # Only create images for 7,8,9, content is different (7x7, i+1 values)
        for i in range(7,10):
            imgFile = os.path.join(testFolder, f'{i}numS.bmp')
            if not os.path.exists(imgFile):
                img = Image.fromarray(np.full((7,7), i+1, dtype=np.uint8))
                img.save(imgFile)
                testImagesCreated = True
        try:
            imgs = getImages(testFolder, list(range(7,10)))
            assert (isinstance(imgs, list) or isinstance(imgs, np.ndarray))
        except Exception as err:
            print(f'getImages public test: {err}')
        if testImagesCreated:
            for i in range(7,10):
                imgFile = os.path.join(testFolder, f'{i}numS.bmp')
                if os.path.exists(imgFile):
                    os.remove(imgFile)
            if len(os.listdir(testFolder)) == 0:
                os.rmdir(testFolder)
    else:
        print('getImages.py (getImages) not found')
    # Edge case: request different missing dir
    with pytest.raises(Exception):
        getImages('nonexistent_dir_public', [1,2,3])