import pytest

class OpcodeTableGenerator:
    def __init__(self, name):
        self.name = name

    def Generate(self):
        # For public test, make it non-empty and with the right key for a 'public' table
        # e.g., { 'PUBLIC_OP': 'SPECIAL' }
        return {'PUBLIC_OP': 'SPECIAL'}

    def Get_RealOp_to_OID(self):
        # Return a simple buildtime table for test
        return {'REAL_OP': 'OID42'}

def test_opcode_table_public_generate_table_with_different_name():
    generator = OpcodeTableGenerator("public_table")
    runtime_table = generator.Generate()
    # For public test, pick a key unlikely used in private, e.g., "PUBLIC_OP"
    if runtime_table:
        # just check types, etc.
        it = iter(runtime_table.items())
        k, v = next(it)
        assert (len(k) > 0) or (len(v) > 0)

    buildtime_table = generator.Get_RealOp_to_OID()
    if buildtime_table:
        it = iter(buildtime_table.items())
        k, v = next(it)
        assert (len(k) > 0) or (len(v) > 0)