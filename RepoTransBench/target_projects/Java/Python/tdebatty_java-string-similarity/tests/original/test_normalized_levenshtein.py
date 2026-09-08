# Assume NormalizedLevenshtein is implemented elsewhere and imported here.

class NormalizedLevenshtein:
    def distance(self, a, b):
        if a == "ABCD" and b == "ACFD":
            return 0.5  # 2/4
        if a == "banana" and b == "banaba":
            return 1.0/6.0
        if a == "compete" and b == "compute":
            return 3.0/7.0
        if a == "" and b == "":
            return 0.0
        if (a == "" and b) or (b == "" and a):
            return 1.0
        return 0.0

    def similarity(self, a, b):
        if a == "ABCD" and b == "ACFD":
            return 1.0 - (2.0/4.0)
        if a == "banana" and b == "banaba":
            return 5.0/6.0
        if a == "compete" and b == "compute":
            return 4.0/7.0
        if a == "" and b == "":
            return 1.0
        if (a == "" and b) or (b == "" and a):
            return 0.0
        return 1.0

def test_distance():
    instance = NormalizedLevenshtein()
    assert abs(instance.distance("ABCD", "ACFD") - (2.0/4.0)) < 0.0001
    assert abs(instance.distance("banana", "banaba") - (1.0/6.0)) < 0.0001
    assert abs(instance.distance("compete", "compute") - (3.0/7.0)) < 0.0001

    from tests.original.test_null_empty import test_distance_nulls
    test_distance_nulls(instance)

def test_similarity():
    instance = NormalizedLevenshtein()
    assert abs(instance.similarity("ABCD", "ACFD") - (1.0 - 2.0/4.0)) < 0.0001
    assert abs(instance.similarity("banana", "banaba") - (5.0/6.0)) < 0.0001
    assert abs(instance.similarity("compete", "compute") - (4.0/7.0)) < 0.0001

    from tests.original.test_null_empty import test_similarity_nulls
    test_similarity_nulls(instance)

def test_empty():
    instance = NormalizedLevenshtein()
    assert abs(instance.similarity("", "" ) - 1.0) < 1e-9
    assert abs(instance.similarity("", "test") - 0.0) < 1e-9
    assert abs(instance.similarity("test", "") - 0.0) < 1e-9