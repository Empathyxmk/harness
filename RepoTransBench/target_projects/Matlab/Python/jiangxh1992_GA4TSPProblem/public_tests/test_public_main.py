import os
import numpy as np
from PIL import Image

try:
    from src.main import main
except ImportError:
    main = None

def test_public_main():
    print('Testing main (public)...')
    if main is not None:
        folder = 'numV'
        created = []
        os.makedirs(folder, exist_ok=True)
        for i in range(10):
            img_filepath = os.path.join(folder, f'{i}numV.bmp')
            if not os.path.exists(img_filepath):
                # 6x6 non-zero values, distinct from original test
                img = Image.fromarray(np.full((6,6), 5+i, dtype=np.uint8))
                img.save(img_filepath)
                created.append(img_filepath)
        try:
            main()
        except Exception as err:
            print(f'main failed (public): {err}')
        # Remove only created images
        for img_filepath in created:
            if os.path.exists(img_filepath):
                os.remove(img_filepath)
        if len(os.listdir(folder)) == 0:
            os.rmdir(folder)
    else:
        print('main.py (main) not found')