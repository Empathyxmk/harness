def import_flyweight():
    from src.Structural.Flyweight import IcecreamFactory
    return IcecreamFactory

def test_create_flyweight_icecream_objects():
    IcecreamFactory = import_flyweight()
    factory = IcecreamFactory()
    vanilla = factory.create_icecream('vanilla', 10)
    assert vanilla.__class__.__name__ == 'Icecream'
    assert vanilla.flavour == 'vanilla'
    assert vanilla.price == 10

def test_return_created_flyweight_objects():
    IcecreamFactory = import_flyweight()
    factory = IcecreamFactory()
    factory.create_icecream('chocolate', 15)
    chocolate = factory.get_icecream('chocolate')
    assert chocolate.__class__.__name__ == 'Icecream'
    assert chocolate.flavour == 'chocolate'
    assert chocolate.price == 15

def test_should_not_create_duplicate_objects():
    IcecreamFactory = import_flyweight()
    factory = IcecreamFactory()
    choco_vanilla = factory.create_icecream('chocolate and vanilla', 15)
    vanilla_choco = factory.create_icecream('chocolate and vanilla', 15)
    assert choco_vanilla is vanilla_choco