def test_default_dex_options_public():
    class DexOpcodes:
        pass
    class DexOptions:
        def __init__(self):
            self.opcodes = DexOpcodes()
            self.enableCache = False
            self.rootDexOnly = False
        @staticmethod
        def getDefault():
            return DexOptions()
    options = DexOptions.getDefault()
    assert options.opcodes is not None
    assert not options.enableCache
    assert not options.rootDexOnly

def test_enable_feature_assignment_public():
    class DexOpcodes:
        pass
    class DexOptions:
        def __init__(self):
            self.opcodes = DexOpcodes()
            self.enableCache = False
            self.rootDexOnly = False
        @staticmethod
        def getDefault():
            return DexOptions()
    options = DexOptions.getDefault()
    options.rootDexOnly = True
    options.enableCache = True
    assert options.rootDexOnly
    assert options.enableCache