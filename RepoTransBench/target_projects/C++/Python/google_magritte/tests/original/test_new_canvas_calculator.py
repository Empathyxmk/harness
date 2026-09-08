import pytest

class NewCanvasCalculatorOptions:
    def __init__(self, scale_factor=None, target_width=None, target_height=None):
        self.scale_factor = scale_factor
        self.target_width = target_width
        self.target_height = target_height

class NewCanvasCalculator:
    @staticmethod
    def get_size_from_options(options, original_width, original_height):
        # Mimic the C++ logic for determining canvas size from options
        # If scale_factor is set, applies scale. Else target_width/height
        if options.scale_factor is not None:
            return (int(original_width * options.scale_factor),
                    int(original_height * options.scale_factor))
        elif options.target_width is not None and options.target_height is not None:
            return (options.target_width, options.target_height)
        elif options.target_width is not None:
            # Maintain aspect ratio
            scale = options.target_width / original_width
            return (options.target_width, int(original_height * scale))
        elif options.target_height is not None:
            scale = options.target_height / original_height
            return (int(original_width * scale), options.target_height)
        else:
            return (original_width, original_height)

import collections

OptionsToSizeTestCase = collections.namedtuple(
    "OptionsToSizeTestCase",
    ["test_name", "options", "original_width", "original_height", "expected"]
)

test_cases = [
    OptionsToSizeTestCase(
        test_name="no_scaling",
        options=NewCanvasCalculatorOptions(),
        original_width=640,
        original_height=480,
        expected=(640, 480)
    ),
    OptionsToSizeTestCase(
        test_name="factor_scaling",
        options=NewCanvasCalculatorOptions(scale_factor=0.5),
        original_width=640,
        original_height=480,
        expected=(320, 240)
    ),
    OptionsToSizeTestCase(
        test_name="only_target_width",
        options=NewCanvasCalculatorOptions(target_width=100),
        original_width=2,
        original_height=1,
        expected=(100, 50)
    ),
    OptionsToSizeTestCase(
        test_name="only_target_height",
        options=NewCanvasCalculatorOptions(target_height=100),
        original_width=2,
        original_height=1,
        expected=(200, 100)
    ),
    OptionsToSizeTestCase(
        test_name="both_target_width_and_height",
        options=NewCanvasCalculatorOptions(target_width=123, target_height=456),
        original_width=640,
        original_height=480,
        expected=(123, 456)
    ),
    OptionsToSizeTestCase(
        test_name="everything_set_factor_takes_precedence",
        options=NewCanvasCalculatorOptions(scale_factor=0.5, target_width=123, target_height=456),
        original_width=640,
        original_height=480,
        expected=(320, 240)
    ),
]

import pytest

@pytest.mark.parametrize("test_case", test_cases, ids=[tc.test_name for tc in test_cases])
def test_get_size_from_options(test_case):
    result = NewCanvasCalculator.get_size_from_options(
        test_case.options,
        test_case.original_width,
        test_case.original_height
    )
    assert result == test_case.expected