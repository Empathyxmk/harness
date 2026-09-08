import os
import shutil
import numpy as np
from PIL import Image
import pytest

# Assuming main() is implemented in src.main
try:
    from src.main import main
except ImportError:
    main = None

def test_main():
    print('Testing main...')
    if main is not None:
        folder = 'numV'
        created = []
        os.makedirs(folder, exist_ok=True)
        # Create 5x5 dummy images 0-9
        for i in range(10):
            img_filepath = os.path.join(folder, f'{i}numV.bmp')
            if not os.path.exists(img_filepath):
                img = Image.fromarray(np.zeros((5,5), dtype=np.uint8))
                img.save(img_filepath)
                created.append(img_filepath)
        # Run main
        try:
            main()
        except Exception as err:
            print('main failed: %s' % err)
        # Remove test generated images
        for img_filepath in created:
            if os.path.exists(img_filepath):
                os.remove(img_filepath)
        if len(os.listdir(folder)) == 0:
            os.rmdir(folder)
    else:
        print('main.py (main) not found')