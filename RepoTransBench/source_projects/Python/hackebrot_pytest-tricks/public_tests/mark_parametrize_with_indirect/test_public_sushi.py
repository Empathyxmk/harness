import pytest

# Patch sys.path so conftest.py in mark_parametrize_with_indirect works correctly
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "code_examples" / "mark_parametrize_with_indirect"))

from code_examples.mark_parametrize_with_indirect.sushi import Sushi
from code_examples.mark_parametrize_with_indirect.conftest import recipes

@pytest.mark.parametrize("roll", [
    "rainbow",
    "spicytuna"
])
def test_recipe_exists_for_roll(roll):
    assert roll in recipes
    s = Sushi(roll, recipes[roll])
    assert s.ingredients == recipes[roll]