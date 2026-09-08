def import_factory():
    from src.Creational.Factory import BallFactory
    return BallFactory

def test_create_basketball_object():
    BallFactory = import_factory()
    factory = BallFactory()
    ball = factory.create_ball('basketball')
    assert ball.__class__.__name__ == 'Basketball'
    assert ball.roll() == 'The basketball is rolling.'
    assert ball.bounce() == 'You bounced the basketball.'

def test_create_football_object_passed_soccer():
    BallFactory = import_factory()
    factory = BallFactory()
    ball = factory.create_ball('soccer')
    assert ball.__class__.__name__ == 'Football'
    assert ball.roll() == 'The football is rolling.'
    assert ball.kick() == 'You kicked the football.'

def test_create_football_object_passed_football():
    BallFactory = import_factory()
    factory = BallFactory()
    ball = factory.create_ball('football')
    assert ball.__class__.__name__ == 'Football'
    assert ball.roll() == 'The football is rolling.'
    assert ball.kick() == 'You kicked the football.'