import pytest

class DummyFunction:
    def __init__(self):
        self.m_function = 0x100  # Arbitrary unique value

    @staticmethod
    def LaunchKernel(args):
        # args is a DummyArguments instance already set to this object
        # Simulate CUDA_SUCCESS as 0
        class DummyValue:
            def IsNumber(self):
                return True
            def NumberValue(self):
                return 0
        return DummyValue()

class DummyArguments(list):
    def push_back(self, value):
        self.append(value)
    def setThis(self, this_obj):
        self.this_object = this_obj
        return self

class DummyV8:
    class MockArray:
        @staticmethod
        def fromInts(lst):
            return {"type": "mockarray", "value": lst}
    class MockBuffer:
        @staticmethod
        def fromRaw(buffer, size):
            # For Python, simply store as a bytes object
            return {"type": "mockbuffer", "value": buffer[:size]}

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_launch_kernel_succeeds_with_different_dims():
    func = DummyFunction()
    args = DummyArguments()
    args.push_back(DummyV8.MockArray.fromInts([4, 3, 2]))
    args.push_back(DummyV8.MockArray.fromInts([2, 2, 2]))
    buffer_bytes = bytes([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16])
    args.push_back(DummyV8.MockBuffer.fromRaw(buffer_bytes, len(buffer_bytes)))
    ret_val = DummyFunction.LaunchKernel(args.setThis(func))
    assert ret_val.IsNumber()
    assert ret_val.NumberValue() == 0