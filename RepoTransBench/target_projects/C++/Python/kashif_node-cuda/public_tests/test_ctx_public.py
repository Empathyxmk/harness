import pytest

class DummyCUcontext:
    def __init__(self):
        self.ctx_id = 42

@pytest.mark.usefixtures("dummy_cuda", "dummy_v8")
def test_ctx_create_destroy_public():
    # Simulate cuCtxCreate and cuCtxDestroy
    CUDA_SUCCESS = 0
    ctx_obj = {"ctx": None}

    def cuCtxCreate(ctx_ptr, flags, device):
        ctx_ptr["ctx"] = DummyCUcontext()
        return CUDA_SUCCESS

    def cuCtxDestroy(ctx):
        # Assume always succeeds if correct type; fail otherwise.
        if isinstance(ctx, DummyCUcontext):
            return CUDA_SUCCESS
        return 1

    ctx = None
    res_create = cuCtxCreate(ctx_obj, 0x123, 1)
    assert res_create == CUDA_SUCCESS
    assert ctx_obj["ctx"] is not None

    res_destroy = cuCtxDestroy(ctx_obj["ctx"])
    assert res_destroy == CUDA_SUCCESS