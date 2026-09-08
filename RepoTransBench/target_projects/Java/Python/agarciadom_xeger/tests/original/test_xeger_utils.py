import random
from src.xeger import Xeger

def test_should_generate_random_number_correctly():
    rnd = random.Random()
    for _ in range(100):
        number = Xeger.getRandomInt(3, 7, rnd)
        assert 3 <= number <= 7