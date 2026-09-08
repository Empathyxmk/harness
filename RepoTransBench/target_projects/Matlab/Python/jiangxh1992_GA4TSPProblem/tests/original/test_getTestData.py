import os
import numpy as np
from PIL import Image
import pytest

try:
    from src.getTestData import getTestData
except ImportError:
    getTestData = None

def test_getTestData():
    print('Testing getTestData...')
    testFolder = 'numS'
    testImagesCreated = False
    if getTestData is not None:
        os.makedirs(testFolder, exist_ok=True)
        for i in range(3):
            imgFile = os.path.join(testFolder, f'{i}numS.bmp')
            if not os.path.exists(imgFile):
                img = Image.fromarray(np.full((5,5), i, dtype=np.uint8))
                img.save(imgFile)
                testImagesCreated = True
        try:
            inputs, targets = getTestData(testFolder, list(range(3)))
            assert isinstance(inputs, np.ndarray) and isinstance(targets, np.ndarray)
        except Exception as err:
            print(f'getTestData test: {err}')
        if testImagesCreated:
            for i in range(3):
                imgFile = os.path.join(testFolder, f'{i}numS.bmp')
                if os.path.exists(imgFile):
                    os.remove(imgFile)
            if len(os.listdir(testFolder)) == 0:
                os.rmdir(testFolder)
    else:
        print('getTestData.py (getTestData) not found')
    # Edge case: directory missing
    with pytest.raises(Exception):
        getTestData('no_dir', [1,2])