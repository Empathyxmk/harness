def import_adapter():
    from src.Structural.Adapter import NewCalculator, OldCalculator, CalcAdapter
    return NewCalculator, OldCalculator, CalcAdapter

def test_should_add():
    NewCalculator, OldCalculator, CalcAdapter = import_adapter()
    old_calc = OldCalculator()
    assert old_calc.operations(10, 5, 'add') == 15
    new_calc = NewCalculator()
    assert new_calc.add(10, 5) == 15
    adapted_calc = CalcAdapter()
    assert adapted_calc.operations(10, 5, 'add') == 15

def test_should_subtract():
    NewCalculator, OldCalculator, CalcAdapter = import_adapter()
    old_calc = OldCalculator()
    assert old_calc.operations(10, 5, 'sub') == 5
    new_calc = NewCalculator()
    assert new_calc.sub(10, 5) == 5
    adapted_calc = CalcAdapter()
    assert adapted_calc.operations(10, 5, 'sub') == 5