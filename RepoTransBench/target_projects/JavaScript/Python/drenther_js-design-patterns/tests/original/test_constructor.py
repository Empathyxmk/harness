def import_constructor():
    from src.Creational.Constructor import Hero
    return Hero

def test_instantiate_and_method_call_works():
    Hero = import_constructor()
    iron_man = Hero('Iron Man', 'fly')
    assert iron_man.get_details() == 'Iron Man can fly'