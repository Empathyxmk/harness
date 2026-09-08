def test_llvmcontext_constructor():
    class DummyLLVMContext:
        pass
    class llvm:
        LLVMContext = DummyLLVMContext
    context = llvm.LLVMContext()
    assert isinstance(context, llvm.LLVMContext)