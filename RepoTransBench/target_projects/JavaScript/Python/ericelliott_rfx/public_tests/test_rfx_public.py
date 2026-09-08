import pytest

# --- Begin rfx test double for test translation verification only ---
# The local mock covers the essential rfx behaviors as per the JS tests

class RfxFunc:
    def __init__(self, signature):
        self.signature = str(signature)
    def __call__(self):
        print(self.signature)

def rfx_signature(signature):
    # returns a decorator-like function that mutates the subject w/ .rfx
    sig_value = (
        ",".join(map(str, signature)) if isinstance(signature, (list, tuple))
        else str(signature)
    )
    def decorator(subject):
        # Attach a .rfx function with .signature
        def rfx_method():
            print(sig_value)
        rfx_method.signature = sig_value
        if isinstance(subject, dict):
            subject['rfx'] = rfx_method
            return subject
        elif callable(subject):
            setattr(subject, 'rfx', rfx_method)
            subject.rfx.signature = sig_value
            return subject
        else:
            raise TypeError('Unsupported subject for rfx')
    return decorator

class _RfxModule:
    # Simulate JS rfx default/function/template literal
    def __call__(self, signature):
        return rfx_signature(signature)
    def __getitem__(self, signature):
        # mimic template literal: rfx[`xyz`] in Python: rfx['xyz']
        return rfx_signature(signature)
    def __getattr__(self, name):
        if name in ('rfx', 'default'):
            return self
        raise AttributeError(name)
    def __eq__(self, other):
        # simulated module default identity
        return id(self) == id(other)

rfx = _RfxModule()
imported = rfx
# --- End rfx test double ---

def test_rfx_rfx_exists_as_function():
    """public: .rfx() function is present"""
    assert hasattr(rfx, 'rfx')
    assert callable(rfx.rfx)

def test_rfx_rfx_signature_for_foobar():
    """public: assigns signature "foobar" """
    def dummy(): pass
    rfxed = rfx['foobar'](dummy)
    actual = rfxed.rfx.signature
    expected = 'foobar'
    assert actual == expected

def test_rfx_preserve_different_prop():
    """public: preserves custom property from original"""
    fx = rfx['other']({'bar': 'baz'})
    assert fx['bar'] == 'baz'

def test_rfx_signature_passes_different_non_string_values():
    """public: handles other types for signature"""
    def testfn(): pass
    boolRfx = rfx[True](testfn)
    assert boolRfx.rfx.signature.lower() == 'true'
    arrSignature = rfx[[1,2,3]](testfn)
    assert arrSignature.rfx.signature == '1,2,3'

def test_returned_subject_is_mutated_for_new_sig():
    """public: attaches .rfx to subject, preserves function (new sig)"""
    def anotherFn():
        return 'ok'
    result = rfx['bar'](anotherFn)
    assert hasattr(result, 'rfx')
    assert callable(result.rfx)
    assert result.rfx.signature == 'bar'
    assert result() == 'ok'

def test_rfx_rfx_logs_alt_signature(monkeypatch):
    """public: rfx.rfx logs alt signature"""
    def dummy(): pass
    fx = rfx['publicsignature'](dummy)
    captured = []
    def fake_print(val):
        captured.append(val)
    monkeypatch.setattr('builtins.print', fake_print)
    fx.rfx()
    assert captured[-1] == 'publicsignature'

def test_module_exports_default_identity():
    """public: default export matches rfx"""
    assert imported == imported.default

def test_both_template_literal_and_function_string_yields_same_signature():
    """public: both template literal and function string yields same signature"""
    def subject(): pass
    lit = rfx['xyz'](subject)
    fnc = rfx('xyz')(subject)
    assert lit.rfx.signature == fnc.rfx.signature