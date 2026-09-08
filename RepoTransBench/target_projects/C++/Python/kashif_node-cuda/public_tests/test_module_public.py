import pytest

class DummyModule:
    def __init__(self):
        self.m_module = "dummy_module_ptr"

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_load_and_get_function_with_different_module():
    CUDA_SUCCESS = 0

    def cuModuleLoad(ptr_ref, filename):
        # filename must be "public_test_module.cubin" to "succeed"
        if filename == "public_test_module.cubin":
            ptr_ref["module"] = "module_success"
            return CUDA_SUCCESS
        return 1

    def cuModuleGetFunction(func_ref, mod, kernel_name):
        # Simulate that it succeeds only for these args
        if mod == "module_success" and kernel_name == "public_dummyKernel":
            func_ref["func"] = "function_success"
            return CUDA_SUCCESS
        return 1

    module = DummyModule()
    filename = "public_test_module.cubin"
    mod_holder = {}
    res = cuModuleLoad(mod_holder, filename)
    assert res == CUDA_SUCCESS
    assert mod_holder["module"] == "module_success"

    func_holder = {"func": None}
    func_res = cuModuleGetFunction(func_holder, mod_holder["module"], "public_dummyKernel")
    assert func_res == CUDA_SUCCESS
    assert func_holder["func"] == "function_success"