import pytest
import numpy as np
from src.genann import *

def test_public_preset_read():
    import os
    save_name = "example/xor.ann"
    if not os.path.exists(save_name):
        pytest.skip(f"Couldn't open file: {save_name}")

    with open(save_name, "rb") as saved:
        ann = genann_read(saved)
    assert ann is not None

    input_data = [[0,0],[0,1],[1,0],[1,1]]
    print("NAND test cases with loaded ANN:")
    for i in range(4):
        print(f"Output for {input_data[i]} is {genann_run(ann, input_data[i])}.")
    genann_free(ann)