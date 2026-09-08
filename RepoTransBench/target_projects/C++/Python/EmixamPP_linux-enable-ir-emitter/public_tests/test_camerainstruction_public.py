import pytest

class CameraInstructionType:
    EXPOSE = 'EXPOSE'
    FOCUS = 'FOCUS'
    UNKNOWN = 'UNKNOWN'
    NONE = 'NONE'

class CameraInstruction:
    def __init__(self, instruction_str):
        # e.g., "EXPOSE,900,1800"
        tokens = instruction_str.split(',')
        self.type = CameraInstructionType.UNKNOWN
        if len(tokens) == 3:
            t = tokens[0].upper()
            if t == CameraInstructionType.EXPOSE:
                self.type = CameraInstructionType.EXPOSE
            elif t == CameraInstructionType.FOCUS:
                self.type = CameraInstructionType.FOCUS
            elif t == CameraInstructionType.UNKNOWN:
                self.type = CameraInstructionType.UNKNOWN
            else:
                # Simulate UNKNOWN or NONE behavior
                self.type = CameraInstructionType.UNKNOWN
            try:
                self.time1 = int(tokens[1])
                self.time2 = int(tokens[2])
            except Exception:
                self.time1 = None
                self.time2 = None
        else:
            # Malformed string; treat all as None
            self.time1 = None
            self.time2 = None

    def __eq__(self, other):
        if not isinstance(other, CameraInstruction):
            return False
        return (
            self.type == other.type and
            self.time1 == other.time1 and
            self.time2 == other.time2
        )

    def __ne__(self, other):
        return not self.__eq__(other)

def test_construct_parse_string():
    # Using distinctly different (but valid) values
    instr1 = CameraInstruction("EXPOSE,900,1800")
    assert instr1.type == CameraInstructionType.EXPOSE
    assert instr1.time1 == 900
    assert instr1.time2 == 1800

    instr2 = CameraInstruction("FOCUS,300,600")
    assert instr2.type == CameraInstructionType.FOCUS
    assert instr2.time1 == 300
    assert instr2.time2 == 600

def test_parse_invalid_type():
    instr = CameraInstruction("PAN,400,800")
    # PAN is not a recognized type; ensure default or error-handling path
    assert instr.type == CameraInstructionType.UNKNOWN or instr.type == CameraInstructionType.NONE
    assert instr.time1 == 400
    assert instr.time2 == 800

def test_equality_operators():
    instr1 = CameraInstruction("EXPOSE,100,200")
    instr2 = CameraInstruction("EXPOSE,100,200")
    instr3 = CameraInstruction("EXPOSE,150,250")
    assert instr1 == instr2
    assert not (instr1 == instr3)
    assert instr1 != instr3