import pytest

def test_interface_blocks_like_structs():
    class UniformBlock:
        def __init__(self):
            self.x = 0.0
    class InputBlock:
        def __init__(self):
            self.y = 0.0
    class OutputBlock:
        def __init__(self):
            self.z = 0.0
    class BufferBlock:
        def __init__(self):
            self.w = 0.0

    # creation
    uniform_block = UniformBlock()
    input_block = InputBlock()
    output_block = OutputBlock()
    buffer_block = BufferBlock()

    # repeated declarations
    uniform_block2 = UniformBlock()
    input_block2 = InputBlock()
    output_block2 = OutputBlock()
    buffer_block2 = BufferBlock()

    uniform_data = uniform_block
    input_data = input_block
    output_data = output_block
    buffer_data = buffer_block

    assert hasattr(uniform_block, 'x')
    assert hasattr(uniform_block2, 'x')
    assert hasattr(input_block, 'y')
    assert hasattr(input_block2, 'y')
    assert hasattr(output_block, 'z')
    assert hasattr(output_block2, 'z')
    assert hasattr(buffer_block, 'w')
    assert hasattr(buffer_block2, 'w')

    assert isinstance(uniform_data, UniformBlock)
    assert isinstance(input_data, InputBlock)
    assert isinstance(output_data, OutputBlock)
    assert isinstance(buffer_data, BufferBlock)