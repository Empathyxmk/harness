import pytest
from src.fritzone_obfy.instr import process_instruction

# Original tests - test process_instruction logic with original data.

def test_process_instruction_gt10():
    assert process_instruction(12) == 24  # 12 > 10 => *2

def test_process_instruction_lt0():
    assert process_instruction(-2) == -1  # <0 => -1

def test_process_instruction_else():
    assert process_instruction(5) == 10   # else => +5