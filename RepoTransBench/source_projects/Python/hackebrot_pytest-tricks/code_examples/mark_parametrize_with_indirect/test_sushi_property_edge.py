from sushi import Sushi

def test_is_vegetarian_with_all_nonveg():
    s = Sushi("Mix", ingredients=["Crab", "Salmon", "Shrimp", "Tuna", "Rice"])
    # Since one non-veg always present, should not be vegetarian
    assert not s.is_vegetarian

def test_is_vegetarian_with_mixed_case():
    # ingredient names are case-sensitive, so "crab" does not match "Crab"
    s = Sushi("Strange", ingredients=["crab", "salmon", "shrimp", "tuna"])
    # None of the "Crab/Salmon/Shrimp/Tuna" proper-case is present
    assert s.is_vegetarian