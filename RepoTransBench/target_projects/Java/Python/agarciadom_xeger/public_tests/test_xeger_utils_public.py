import random
from src.xeger import Xeger

def test_should_generate_random_number_correctly_public():
    rnd = random.Random()
    for _ in range(100):
        number = Xeger.getRandomInt(8, 11, rnd)
        assert 8 <= number <= 11