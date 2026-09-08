def test_initialize_native_target():
    # These are dummy 'calls' as there's no native logic in Python
    called = []
    def dummy(): called.append("called")
    llvm = type("llvm", (), {
        "InitializeNativeTarget": dummy,
        "InitializeNativeTargetAsmPrinter": dummy,
        "InitializeNativeTargetAsmParser": dummy,
        "InitializeNativeTargetDisassembler": dummy,
    })()
    llvm.InitializeNativeTarget()
    llvm.InitializeNativeTargetAsmPrinter()
    llvm.InitializeNativeTargetAsmParser()
    llvm.InitializeNativeTargetDisassembler()
    assert len(called) == 4

def test_initialize_all_targets():
    called = []
    def dummy(): called.append("called")
    llvm = type("llvm", (), {
        "InitializeAllTargetInfos": dummy,
        "InitializeAllTargets": dummy,
        "InitializeAllTargetMCs": dummy,
        "InitializeAllAsmPrinters": dummy,
        "InitializeAllAsmParsers": dummy,
        "InitializeAllDisassemblers": dummy,
    })()
    llvm.InitializeAllTargetInfos()
    llvm.InitializeAllTargets()
    llvm.InitializeAllTargetMCs()
    llvm.InitializeAllAsmPrinters()
    llvm.InitializeAllAsmParsers()
    llvm.InitializeAllDisassemblers()
    assert len(called) == 6