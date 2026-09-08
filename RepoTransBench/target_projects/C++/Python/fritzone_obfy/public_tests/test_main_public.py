import pytest
from src.fritzone_obfy.instr import process_instruction

# Public tests - Same logic, different data for process_instruction.

def test_process_instruction_gt10_public():
    assert process_instruction(15) == 30   # 15 > 10 => *2, new data

def test_process_instruction_lt0_public():
    assert process_instruction(-7) == -1   # -7 < 0 => -1, new data

def test_process_instruction_else_public():
    assert process_instruction(6) == 11    # 6 within [0,10] => +5, new data