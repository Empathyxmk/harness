def test_multiset_and_set():
    from collections import Counter
    import sys
    import io

    # MultiSet (Counter-based)
    table = []
    table.append(1)
    table.append(2)
    table.append(2)
    table.append(2)
    table.append(2)
    table.append(-5)
    table.append(3)
    table.append(-5)
    multi = Counter(table)
    twos_cnt = multi[2]
    assert twos_cnt == 4
    assert multi[-5] == 2
    # Simulating lower_bound and upper_bound: all 2's
    twos = [x for x in table if x == 2]
    assert len(twos) == 4
    # Remove all 2s
    table2 = [x for x in table if x != 2]
    multi2 = Counter(table2)
    assert multi2[2] == 0
    # Simulate Set insert/erase/find/min/max
    s = set()
    s.add(1)
    s.add(3)
    s.add(5)
    s.add(4)
    res_4 = 4 in s
    res_new_ins = 6 not in s
    s.add(6)
    res_7 = 7 not in s
    s.add(7)
    res_find3 = 3 in s
    res_find2 = 2 in s
    res_find4 = 4 in s
    s.discard(3)
    res_find3_after = 3 in s
    minval = min(s)
    maxval = max(s)
    s_list = sorted(list(s))
    # Check
    assert res_4
    assert res_new_ins
    assert res_7
    assert res_find3
    assert not res_find2
    assert res_find4
    assert not res_find3_after
    assert minval == 1
    assert maxval == max(s)
    # Iterating over set (should have several numbers)
    assert all(isinstance(i, int) for i in s)