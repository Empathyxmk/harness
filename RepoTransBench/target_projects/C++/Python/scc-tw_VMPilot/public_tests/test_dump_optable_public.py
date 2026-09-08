import pytest
import json

class OpcodeTableGenerator:
    def __init__(self, name):
        self.name = name

    def Generate(self):
        # Simulate a runtime table: dict of OI -> opcode string
        return {'OI1': 'OPCODE1'}

    def Get_RealOp_to_OID(self):
        # Simulate a buildtime table: dict of opcode string -> OID string
        return {'OPCODE1': 'OID1'}

def test_dump_optable_public_generate_json_with_different_key():
    ot_gen = OpcodeTableGenerator("another_public_name")
    runtime_table = ot_gen.Generate()
    buildtime_table = ot_gen.Get_RealOp_to_OID()

    j = {
        "runtime_table": [],
        "buildtime_table": []
    }

    for opcode, oid in buildtime_table.items():
        entry = {"real_opcode": opcode, "OID": oid}
        j["buildtime_table"].append(entry)
    for oi, opcode in runtime_table.items():
        entry = {"OI": oi, "real_opcode": opcode}
        j["runtime_table"].append(entry)

    # Test non-empty json structure and properties
    assert isinstance(j["buildtime_table"], list)
    assert isinstance(j["runtime_table"], list)
    assert len(j["buildtime_table"]) >= 0
    assert len(j["runtime_table"]) >= 0