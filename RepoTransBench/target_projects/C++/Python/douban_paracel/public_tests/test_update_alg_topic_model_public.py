def dict_update(a, b):
    merged = dict(a)
    idx = max(merged.values(), default=-1) + 1 if merged else 0
    for k in b:
        if k not in merged:
            merged[k] = idx
            idx += 1
    return merged

def topic_update(a, b):
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

def test_dict_update_basic_merge_public():
    a = {"apple": 0, "banana": 1}
    b = {"banana": 4, "pear": 9, "grape": 2}
    merged = dict_update(a, b)
    assert merged["apple"] == 0
    assert merged["banana"] == 1
    assert merged["pear"] == 2
    assert merged["grape"] == 3
    assert len(merged) == 4

def test_dict_update_empty_b():
    a = {"sun": 0}
    b = {}
    merged = dict_update(a, b)
    assert merged["sun"] == 0
    assert len(merged) == 1

def test_topics_update_correct_sum_public():
    a = [[2, 4, 6], [8, 10, 12]]
    b = [[1, 3, 5], [7, 9, 11]]
    result = topic_update(a, b)
    assert result[0][0] == 3
    assert result[0][1] == 7
    assert result[0][2] == 11
    assert result[1][0] == 15
    assert result[1][1] == 19
    assert result[1][2] == 23

def test_word_update_correct_sum_public():
    a = [3, 4, 5, 6]
    b = [10, 20, 30, 40]
    result = word_update(a, b)
    assert result[0] == 13
    assert result[1] == 24
    assert result[2] == 35
    assert result[3] == 46

def test_sum_topic_update_negative():
    assert sum_topic_update(-5, 7) == 2
    assert sum_topic_update(-5, -4) == -9

def test_key_filter_public():
    assert key_filter("key_secret_abc") is True
    assert key_filter("notakey_123") is False