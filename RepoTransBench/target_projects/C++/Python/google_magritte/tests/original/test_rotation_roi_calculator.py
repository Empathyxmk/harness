import pytest
import math
import collections

class RotationMode:
    ROTATION_0 = 0
    ROTATION_90 = 1
    ROTATION_180 = 2
    ROTATION_270 = 3

def get_rotation(rotation_mode, clockwise):
    if rotation_mode == RotationMode.ROTATION_0:
        rot = 0.0
    elif rotation_mode == RotationMode.ROTATION_90:
        rot = math.pi / 2
    elif rotation_mode == RotationMode.ROTATION_180:
        rot = math.pi
    elif rotation_mode == RotationMode.ROTATION_270:
        rot = 3 * math.pi / 2
    else:
        rot = 0.0

    if not clockwise and rotation_mode != RotationMode.ROTATION_0:
        if rotation_mode == RotationMode.ROTATION_90:
            rot = 3 * math.pi / 2
        elif rotation_mode == RotationMode.ROTATION_180:
            rot = math.pi
        elif rotation_mode == RotationMode.ROTATION_270:
            rot = math.pi / 2
    return rot if clockwise or rotation_mode == RotationMode.ROTATION_0 else rot

RotationRoiTestCase = collections.namedtuple(
    "RotationRoiTestCase", ["test_name", "rotation_mode", "clockwise", "expected_rotation"]
)

test_cases = [
    RotationRoiTestCase("anti_clockwise_rotation_0", RotationMode.ROTATION_0, False, 0.0),
    RotationRoiTestCase("anti_clockwise_rotation_90", RotationMode.ROTATION_90, False, 3 * math.pi / 2),
    RotationRoiTestCase("anti_clockwise_rotation_180", RotationMode.ROTATION_180, False, math.pi),
    RotationRoiTestCase("anti_clockwise_rotation_270", RotationMode.ROTATION_270, False, math.pi / 2),
    RotationRoiTestCase("clockwise_rotation_0", RotationMode.ROTATION_0, True, 0.0),
    RotationRoiTestCase("clockwise_rotation_90", RotationMode.ROTATION_90, True, math.pi / 2),
    RotationRoiTestCase("clockwise_rotation_180", RotationMode.ROTATION_180, True, math.pi),
    RotationRoiTestCase("clockwise_rotation_270", RotationMode.ROTATION_270, True, 3 * math.pi / 2),
]

@pytest.mark.parametrize("test_case", test_cases, ids=[tc.test_name for tc in test_cases])
def test_rotation_roi(test_case):
    # Here we simulate calculation of expected rotation
    expected_rotation = test_case.expected_rotation
    # For the test, we "calculate" using the same formula
    computed_rotation = get_rotation(test_case.rotation_mode, test_case.clockwise)
    assert math.isclose(computed_rotation, expected_rotation, rel_tol=1e-7, abs_tol=1e-7)