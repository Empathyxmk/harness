import pytest

# Patch sys.path so conftest.py in mark_parametrize_with_indirect works correctly
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "code_examples" / "mark_parametrize_with_indirect"))

from code_examples.mark_parametrize_with_indirect.sushi import Sushi
from code_examples.mark_parametrize_with_indirect.conftest import recipes

@pytest.mark.parametrize("sushi,expected_ingredients", [
    ("spicytuna", ["tuna", "sriracha", "scallions"]),
    ("rainbow", ["tuna", "avocado", "shrimp", "salmon"]),
])
def test_conftest_py_recipe(sushi, expected_ingredients):
    roll = Sushi(sushi, recipes[sushi])
    assert roll.ingredients == expected_ingredients