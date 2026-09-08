import random
import re
from src.xeger import Xeger, FailedRandomWalkException

def test_should_generate_text_correctly():
    regex = "[ab]{4,6}c"
    generator = Xeger(regex)
    for _ in range(100):
        text = generator.generate()
        assert re.fullmatch(regex, text)

def test_repeatable_regex():
    for _ in range(1000):
        generator = Xeger("[ab]{4,6}c", random.Random(1000))
        generator2 = Xeger("[ab]{4,6}c", random.Random(1000))

        firstList = [generator.generate() for _ in range(100)]
        secondList = [generator2.generate() for _ in range(100)]
        assert firstList == secondList

def test_walk_range():
    for _ in range(100):
        generator = Xeger("[ab]{0,100}c", random.Random(1000))
        generator2 = Xeger("[ab]{0,100}c", random.Random(1000))

        def generate_regex(gen, cnt, min_length, max_length):
            out = []
            for __ in range(cnt):
                try:
                    out.append(gen.generate(min_length, max_length))
                except FailedRandomWalkException:
                    out.append(None)
            return out

        firstList = generate_regex(generator, 100, 0, 100)
        secondList = generate_regex(generator2, 100, 0, 100)
        assert len(firstList) == len(secondList)
        assert firstList == secondList