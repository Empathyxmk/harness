def test_simple_compile_test_public_variant():
    from enum import Enum
    class ColorPublic(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3

    assert ColorPublic['GREEN'] == ColorPublic.GREEN