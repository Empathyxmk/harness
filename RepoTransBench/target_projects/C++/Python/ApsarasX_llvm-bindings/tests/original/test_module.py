import pytest

class DummyLLVMContext:
    pass

class DummyFunctionType:
    @staticmethod
    def get(void_type, is_var_arg):
        return DummyFunctionType()

class DummyType:
    @staticmethod
    def getVoidTy(context):
        return "void"

class DummyFunction:
    LinkageTypes = type("LinkageTypes", (), {"ExternalLinkage": 0})
    @staticmethod
    def Create(func_type, linkage, name, module):
        return DummyFunction()
    def __init__(self):
        self.func_type = None

class DummyFunctionCallee:
    def getFunctionType(self):
        return DummyFunctionType()

class DummyBasicBlock:
    @staticmethod
    def Create(context, name, func):
        return DummyBasicBlock()

class DummyGlobalVariable:
    def __init__(self, module, constant_type, constant_bool, linkage, constant, name):
        pass

class DummyConstantInt:
    @staticmethod
    def get(constant_type, value):
        return value

class DummyModule:
    ModFlagBehavior = type("ModFlagBehavior", (), {"Require": 1})
    def __init__(self, name, context):
        self.identifier = name
        self.context = context
        self.source_filename = name
        self.data_layout = ''
        self.target_triple = ''
        self.funcs = {}
        self.globals = {}
        self.flags = []
        self.is_empty = True

    def getModuleIdentifier(self):
        return self.identifier

    def setModuleIdentifier(self, module_id=None):
        if module_id is None or not isinstance(module_id, str):
            raise ValueError("Module.setModuleIdentifier needs to be called with: (moduleID: string)")
        self.identifier = module_id

    def getSourceFileName(self):
        return self.source_filename

    def setSourceFileName(self, source_file_name=None):
        if source_file_name is None or not isinstance(source_file_name, str):
            raise ValueError("Module.setSourceFileName needs to be called with: (sourceFileName: string)")
        self.source_filename = source_file_name

    def getName(self):
        return self.identifier

    def getDataLayoutStr(self):
        return self.data_layout

    def setDataLayout(self, layout=None):
        if layout is None or not isinstance(layout, str):
            raise ValueError("Module.setDataLayout needs to be called with:\n\t - (desc: string)\n\t - (dataLayout: DataLayout)")
        self.data_layout = layout

    def getTargetTriple(self):
        return self.target_triple

    def setTargetTriple(self, ttriple=None):
        if ttriple is None or not isinstance(ttriple, str):
            raise ValueError("Module.setTargetTriple needs to be called with: (targetTriple: string)")
        self.target_triple = ttriple

    def getOrInsertFunction(self, name=None, func_type=None):
        if name is None or not isinstance(name, str) or func_type is None or not isinstance(func_type, DummyFunctionType):
            raise ValueError("Module.getOrInsertFunction needs to be called with: (name: string, fnType: FunctionType)")
        if name not in self.funcs:
            func = DummyFunction()
            self.funcs[name] = func
        return DummyFunctionCallee()

    def getFunction(self, name=None):
        if name is None or not isinstance(name, str):
            raise ValueError("Module.getFunction needs to be called with: (name: string)")
        return self.funcs.get(name, None)

    def getGlobalVariable(self, name=None, allowInternal=None):
        if name is None or not isinstance(name, str):
            raise ValueError("Module.getGlobalVariable needs to be called with: (name: string, allowInternal?: boolean)")
        return self.globals.get(name, None)

    def addModuleFlag(self, behavior=None, key=None, value=None):
        if behavior is None or not isinstance(behavior, int) or not (1 <= behavior <= 7) or key is None or not isinstance(key, str) or value is None or not isinstance(value, int):
            raise ValueError("Module.addModuleFlag needs to be called with (behavior: number, key: string, value: number)\n\t - limit: behavior should belong to [1, 7]")
        self.flags.append((behavior, key, value))

    def empty(self):
        return self.is_empty

    def print(self):
        # Dummy print for snapshot
        return f'''; ModuleID = '{self.identifier}'
source_filename = "{self.source_filename}"

define void @func() {{
entry:
}}
'''

class llvm:
    LLVMContext = DummyLLVMContext
    Module = DummyModule
    FunctionType = DummyFunctionType
    Type = DummyType
    Function = DummyFunction
    FunctionCallee = DummyFunctionCallee
    BasicBlock = DummyBasicBlock
    GlobalVariable = DummyGlobalVariable
    ConstantInt = DummyConstantInt

def test_module_constructor_normal():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert isinstance(module, llvm.Module)

def test_module_constructor_not_enough_args():
    with pytest.raises(TypeError):
        llvm.Module()
    with pytest.raises(TypeError):
        llvm.Module("Module.spec.ts")

def test_module_constructor_wrong_types():
    with pytest.raises(TypeError):
        llvm.Module(1, llvm.LLVMContext())
    with pytest.raises(TypeError):
        llvm.Module("Module.spec.ts", {})

def test_module_set_get_module_identifier():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getModuleIdentifier() == "Module.spec.ts"
    module.setModuleIdentifier("module")
    assert module.getModuleIdentifier() == "module"

def test_module_setmoduleidentifier_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match="Module.setModuleIdentifier needs to be called with: \(moduleID: string\)"):
        module.setModuleIdentifier()

def test_module_setmoduleidentifier_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match="Module.setModuleIdentifier needs to be called with: \(moduleID: string\)"):
        module.setModuleIdentifier(1)

def test_module_set_get_sourcefilename():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getSourceFileName() == "Module.spec.ts"
    module.setSourceFileName("test.cpp")
    assert module.getSourceFileName() == "test.cpp"

def test_module_setsourcefilename_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match="Module.setSourceFileName needs to be called with: \(sourceFileName: string\)"):
        module.setSourceFileName()

def test_module_setsourcefilename_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match="Module.setSourceFileName needs to be called with: \(sourceFileName: string\)"):
        module.setSourceFileName(1)

def test_module_get_name():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getName() == "Module.spec.ts"

def test_module_set_get_datalayout():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getDataLayoutStr() == ''
    datalayout = 'e-m:e-p270:32:32-p271:32:32-p272:64:64-i64:64-f80:128-n8:16:32:64-S128'
    module.setDataLayout(datalayout)
    assert module.getDataLayoutStr() == datalayout

def test_module_setdatalayout_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match=r"Module.setDataLayout needs to be called with:"):
        module.setDataLayout()

def test_module_setdatalayout_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match=r"Module.setDataLayout needs to be called with:"):
        module.setDataLayout(1)

def test_module_set_get_targettriple():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getTargetTriple() == ''
    targettriple = "x86_64-pc-linux-gnu"
    module.setTargetTriple(targettriple)
    assert module.getTargetTriple() == targettriple

def test_module_settargettriple_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match="Module.setTargetTriple needs to be called with: \(targetTriple: string\)"):
        module.setTargetTriple()

def test_module_settargettriple_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError, match="Module.setTargetTriple needs to be called with: \(targetTriple: string\)"):
        module.setTargetTriple(1)

def test_module_getorinsertfunction_new():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    func_type = llvm.FunctionType.get(llvm.Type.getVoidTy(context), False)
    func_callee = module.getOrInsertFunction("func", func_type)
    # Since our dummy always returns DummyFunctionCallee, check class
    assert isinstance(func_callee, llvm.FunctionCallee)

def test_module_getorinsertfunction_existing():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    func_type = llvm.FunctionType.get(llvm.Type.getVoidTy(context), False)
    module.funcs["func"] = llvm.Function.Create(func_type, llvm.Function.LinkageTypes.ExternalLinkage, "func", module)
    func_callee = module.getOrInsertFunction("func", llvm.FunctionType.get(llvm.Type.getVoidTy(context), False))
    assert isinstance(func_callee, llvm.FunctionCallee)

def test_module_getorinsertfunction_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.getOrInsertFunction()
    with pytest.raises(ValueError):
        module.getOrInsertFunction('func')

def test_module_getorinsertfunction_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    func_type = llvm.FunctionType.get(llvm.Type.getVoidTy(context), False)
    with pytest.raises(ValueError):
        module.getOrInsertFunction(1, func_type)
    with pytest.raises(ValueError):
        module.getOrInsertFunction('func', 1)
    with pytest.raises(ValueError):
        module.getOrInsertFunction(1, 1)

def test_module_getfunction_normal():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    func_type = llvm.FunctionType.get(llvm.Type.getVoidTy(context), False)
    func = llvm.Function.Create(func_type, llvm.Function.LinkageTypes.ExternalLinkage, "func", module)
    module.funcs["func"] = func
    assert module.getFunction("func") == func

def test_module_getfunction_nosuch():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getFunction("func") is None

def test_module_getfunction_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.getFunction()

def test_module_getfunction_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.getFunction(1)

def test_module_getglobalvariable_normal():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    constant_type = "int32"
    constant = 23
    gv = llvm.GlobalVariable(module, constant_type, True, llvm.Function.LinkageTypes.ExternalLinkage, constant, "globalVar")
    module.globals["globalVar"] = gv
    assert isinstance(module.getGlobalVariable("globalVar"), llvm.GlobalVariable)

def test_module_getglobalvariable_nosuch():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.getGlobalVariable("globalVar") is None

def test_module_getglobalvariable_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.getGlobalVariable()

def test_module_getglobalvariable_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.getGlobalVariable(1)

def test_module_addmoduleflag_normal():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    module.addModuleFlag(1, "name", 1)

def test_module_addmoduleflag_not_enough_args():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.addModuleFlag()
    with pytest.raises(ValueError):
        module.addModuleFlag(1)
    with pytest.raises(ValueError):
        module.addModuleFlag(1, "name")

def test_module_addmoduleflag_wrong_types():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    with pytest.raises(ValueError):
        module.addModuleFlag("param1", "name", 1)
    with pytest.raises(ValueError):
        module.addModuleFlag(1, 2, 1)
    with pytest.raises(ValueError):
        module.addModuleFlag(1, "name", "param3")

def test_module_empty_true():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    assert module.empty() is True

def test_module_empty_false():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    module.is_empty = False
    assert module.empty() is False

def test_module_print_snapshot():
    context = llvm.LLVMContext()
    module = llvm.Module("Module.spec.ts", context)
    func_type = llvm.FunctionType.get(llvm.Type.getVoidTy(context), False)
    func = llvm.Function.Create(func_type, llvm.Function.LinkageTypes.ExternalLinkage, "func", module)
    DummyBasicBlock.Create(context, "entry", func)
    out = module.print()
    # Instead of snapshot, ensure output string follows the structure
    assert out.startswith("; ModuleID = 'Module.spec.ts'")
    assert "source_filename = \"Module.spec.ts\"" in out
    assert "define void @func()" in out