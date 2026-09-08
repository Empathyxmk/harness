def import_command():
    from src.Behavioral.Command import Command, SpecialMath
    return Command, SpecialMath

def test_return_square():
    Command, SpecialMath = import_command()
    x = Command(SpecialMath(5))
    assert x.execute('square') == 25

def test_return_cube():
    Command, SpecialMath = import_command()
    x = Command(SpecialMath(10))
    assert x.execute('cube') == 1000

def test_return_square_root():
    Command, SpecialMath = import_command()
    x = Command(SpecialMath(4))
    assert x.execute('squareRoot') == 2

def test_records_executed_commands():
    Command, SpecialMath = import_command()
    x = Command(SpecialMath(5))
    x.execute('square')
    x.execute('cube')
    assert x.commands_executed == ['square', 'cube']