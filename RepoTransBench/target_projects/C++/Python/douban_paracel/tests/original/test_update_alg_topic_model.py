import pytest

def dict_update(a, b):
    # Merge the two dictionaries as in the C++ version for topic models.
    # a: dict[str, int], b: dict[str, int]
    merged = dict(a)
    idx = max(merged.values(), default=-1) + 1 if merged else 0
    for k in b:
        if k not in merged:
            merged[k] = idx
            idx += 1
    return merged

def topic_update(a, b):
    # Element-wise sum of two 2d integer arrays
    return [
        [a[i][j] + b[i][j] for j in range(len(a[0]))]
        for i in range(len(a))
    ]

def word_update(a, b):
    return [a[i] + b[i] for i in range(len(a))]

def sum_topic_update(a, b):
    return a + b

def key_filter(key):
    return key.startswith("key_")

def test_dict_update_basic_merge():
    a = {"word1": 0, "word2": 1}
    b = {"word2": 5, "word3": 9, "word4": 2}
    merged = dict_update(a, b)
    assert merged["word1"] == 0
    assert merged["word2"] == 1
    assert merged["word3"] == 2
    assert merged["word4"] == 3
    assert len(merged) == 4

def test_dict_update_empty_a():
    a = {}
    b = {"foo": 1, "bar": 2}
    merged = dict_update(a, b)
    assert merged["foo"] == 0
    assert merged["bar"] == 1
    assert len(merged) == 2

def test_topics_update_correct_sum():
    a = [[1, 2], [3, 4]]
    b = [[5, 6], [7, 8]]
    result = topic_update(a, b)
    assert result[0][0] == 6
    assert result[0][1] == 8
    assert result[1][0] == 10
    assert result[1][1] == 12

def test_word_update_correct_sum():
    a = [1, 1, 2]
    b = [2, 2, 3]
    result = word_update(a, b)
    assert result[0] == 3
    assert result[1] == 3
    assert result[2] == 5

def test_sum_topic_update():
    assert sum_topic_update(5, 7) == 12
    assert sum_topic_update(-1, 1) == 0

def test_key_filter_true():
    assert key_filter("key_hello") is True

def test_key_filter_false():
    assert key_filter("notakey") is False
    assert key_filter("") is False
    assert key_filter("kEy_key_") is False  # case sensitive