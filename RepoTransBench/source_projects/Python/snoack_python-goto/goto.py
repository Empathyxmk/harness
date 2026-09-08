import dis
import types
import array
import sys

__all__ = ["with_goto"]

def _array_to_bytes(a):
    try:
        return a.tobytes()
    except AttributeError:
        return a.tostring()

class _Bytecode(object):
    def __init__(self):
        if hasattr(dis, "opmap"):  # Python 3
            self.argument = "oparg"
            self.argument_bits = 8
            self.opmap = dis.opmap
            self.opname = dis.opname
        else:
            self.argument = "arg"
            self.argument_bits = 8
            self.opmap = {}
            self.opname = []

    def __repr__(self):
        return "<_Bytecode argument_bits=%r>" % (self.argument_bits,)

_BYTECODE = _Bytecode()

def _get_posonlyargcount(code):
    # Portable for Python 3.8+
    if hasattr(code, "co_posonlyargcount"):
        return code.co_posonlyargcount
    return 0

def _make_code(code, codestring):
    if code is None:
        raise TypeError("Code argument must not be None")
    if sys.version_info >= (3, 11):
        return types.CodeType(
            code.co_argcount,
            _get_posonlyargcount(code),
            code.co_kwonlyargcount,
            code.co_nlocals,
            code.co_stacksize,
            code.co_flags,
            codestring,
            code.co_consts,
            code.co_names,
            code.co_varnames,
            code.co_filename,
            code.co_name,
            code.co_qualname if hasattr(code, "co_qualname") else code.co_name,
            code.co_firstlineno,
            code.co_linetable if hasattr(code, "co_linetable") else code.co_lnotab,
            code.co_exceptiontable if hasattr(code, "co_exceptiontable") else b'',
            code.co_freevars,
            code.co_cellvars
        )
    elif sys.version_info >= (3, 8):
        return types.CodeType(
            code.co_argcount,
            _get_posonlyargcount(code),
            code.co_kwonlyargcount,
            code.co_nlocals,
            code.co_stacksize,
            code.co_flags,
            codestring,
            code.co_consts,
            code.co_names,
            code.co_varnames,
            code.co_filename,
            code.co_name,
            code.co_firstlineno,
            code.co_lnotab,
            code.co_freevars,
            code.co_cellvars
        )
    elif sys.version_info >= (3, 0):
        return types.CodeType(
            code.co_argcount,
            code.co_kwonlyargcount,
            code.co_nlocals,
            code.co_stacksize,
            code.co_flags,
            codestring,
            code.co_consts,
            code.co_names,
            code.co_varnames,
            code.co_filename,
            code.co_name,
            code.co_firstlineno,
            code.co_lnotab,
            code.co_freevars,
            code.co_cellvars
        )
    else:
        return types.CodeType(
            code.co_argcount,
            code.co_nlocals,
            code.co_stacksize,
            code.co_flags,
            codestring,
            code.co_consts,
            code.co_names,
            code.co_varnames,
            code.co_filename,
            code.co_name,
            code.co_firstlineno,
            code.co_lnotab,
            code.co_freevars,
            code.co_cellvars
        )

def _parse_instructions(co_code):
    i = 0
    n = len(co_code)
    while i < n:
        op = co_code[i]
        if not isinstance(op, int):
            op = ord(op)
        i += 1
        arg = None
        if op >= dis.HAVE_ARGUMENT:
            arg = co_code[i] + (co_code[i+1]<<8)
            i += 2
        yield dis.opname[op], arg, i-3 if arg is not None else i-1

def _get_instruction_size(opname, oparg=None):
    op = dis.opmap.get(opname)
    if op is None:
        raise ValueError("Unknown opname: %r" % opname)
    if oparg is not None and oparg > 0xFFFF:
        # EXTENDED_ARG
        return 6
    return 3 if op >= dis.HAVE_ARGUMENT else 1

def _get_instructions_size(ops):
    size = 0
    for op in ops:
        if isinstance(op, tuple):
            opname, oparg = op
        else:
            opname, oparg = op, None
        size += _get_instruction_size(opname, oparg)
    return size

def _write_instruction(buf, offset, opname, oparg=None):
    opnum = dis.opmap.get(opname)
    if opnum is None:
        raise ValueError("Unknown opname: %r" % opname)
    i = offset
    buf[i] = opnum
    i += 1
    if opnum >= dis.HAVE_ARGUMENT:
        if oparg is None:
            oparg1 = oparg2 = 0
        elif oparg > 0xFFFF:
            buf[i] = dis.opmap["EXTENDED_ARG"]
            buf[i + 1] = (oparg >> 16) & 0xFF
            buf[i + 2] = (oparg >> 8) & 0xFF
            buf[i + 3] = oparg & 0xFF
            i += 4
            return
        else:
            oparg1 = oparg & 0xff
            oparg2 = (oparg >> 8) & 0xff
        buf[i] = oparg1
        buf[i + 1] = oparg2

def _write_instructions(buf, offset, ops):
    i = offset
    for op in ops:
        if isinstance(op, tuple):
            opname, oparg = op
        else:
            opname, oparg = op, None
        _write_instruction(buf, i, opname, oparg)
        sz = _get_instruction_size(opname, oparg)
        i += sz

def _find_labels_and_gotos(code):
    labels = {}
    gotos = []
    for i, instr in enumerate(code):
        if isinstance(instr, tuple) and instr[0] == "label":
            labels[instr[1]] = i
        elif isinstance(instr, tuple) and instr[0] == "goto":
            gotos.append((i, instr[1]))
    return labels, gotos

def with_goto(func_or_code):
    if not (hasattr(func_or_code, "__code__") or isinstance(func_or_code, types.CodeType)):
        raise TypeError("Expected function or code object")
    if hasattr(func_or_code, "goto_mark") and getattr(func_or_code, "goto_mark"):
        return func_or_code

    def _patch_code(code):
        buf = array.array("B", code.co_code)
        return _make_code(code, _array_to_bytes(buf))
    if isinstance(func_or_code, types.CodeType):
        return _patch_code(func_or_code)
    else:
        import functools
        code = func_or_code.__code__
        newcode = _patch_code(code)
        newfunc = types.FunctionType(
            newcode,
            func_or_code.__globals__,
            func_or_code.__name__,
            func_or_code.__defaults__,
            func_or_code.__closure__,
        )
        newfunc.__dict__.update(func_or_code.__dict__)
        newfunc.goto_mark = True
        functools.update_wrapper(newfunc, func_or_code)
        return newfunc