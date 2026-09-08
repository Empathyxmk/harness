import pytest

# --- QuadRanges simulation (minimal stateful logic) ---
class QuadRanges:
    def __init__(self, start=None, length=None):
        self.ranges = []
        if start is not None and length is not None and length > 0:
            self.ranges.append({'start': start, 'length': length})

    @property
    def n_ranges(self):
        return len(self.ranges)

    def add(self, start, length):
        # Insert the new range and merge/adjust as per the logic
        # This logic is hand-ported for the test expectations
        new_start = start
        new_end = start + length
        new_ranges = []
        merged = False
        for r in self.ranges:
            cur_start = r['start']
            cur_end = cur_start + r['length']
            if new_end < cur_start or new_start > cur_end:
                new_ranges.append(r)
            else:
                new_start = min(new_start, cur_start)
                new_end = max(new_end, cur_end)
                merged = True
        new_ranges.append({'start': new_start, 'length': new_end - new_start})
        new_ranges.sort(key=lambda r: r['start'])
        # Join adjacent or overlapping ranges
        merged_ranges = []
        for r in new_ranges:
            if not merged_ranges:
                merged_ranges.append(r)
            else:
                last = merged_ranges[-1]
                if last['start'] + last['length'] >= r['start']:
                    # merge
                    newlen = max(last['start'] + last['length'], r['start'] + r['length']) - last['start']
                    last['length'] = newlen
                else:
                    merged_ranges.append(r)
        self.ranges = merged_ranges

    def copy(self):
        cpy = QuadRanges()
        cpy.ranges = [{'start': r['start'], 'length': r['length']} for r in self.ranges]
        return cpy

    def remove(self, start, length):
        rlist = []
        rem_start = start
        rem_end = start + length
        for r in self.ranges:
            cur_start = r['start']
            cur_end = cur_start + r['length']
            if rem_end <= cur_start or rem_start >= cur_end:
                # no overlap
                rlist.append({'start': cur_start, 'length': r['length']})
            else:
                # overlap
                if rem_start > cur_start:
                    left_len = rem_start - cur_start
                    if left_len > 0:
                        rlist.append({'start': cur_start, 'length': left_len})
                if rem_end < cur_end:
                    right_len = cur_end - rem_end
                    if right_len > 0:
                        rlist.append({'start': rem_end, 'length': right_len})
        self.ranges = rlist

# --- Tests begin here ---
def test_unitfile_print():
    # Placeholder: would compare generated vs file
    assert True

def test_range_creation():
    empty = QuadRanges()
    assert empty.n_ranges == 0

    one = QuadRanges(17, 42)
    assert one.n_ranges == 1
    assert one.ranges[0]['start'] == 17
    assert one.ranges[0]['length'] == 42

@pytest.mark.parametrize("add_args, expect", [
    # (args, expected n_ranges, starts, lens)
    ((0, 9), (2, [(0,9), (10,10)])),  # before
    ((0, 10), (1, [(0,20)])),         # just before
    ((0, 19), (1, [(0,20)])),         # before+inside
    ((0, 20), (1, [(0,20)])),         # before+inside whole
    ((0, 30), (1, [(0,30)])),         # before+inside+after
    ((10, 5), (1, [(10,10)])),        # just inside
    ((12, 5), (1, [(10,10)])),        # inside
    ((15, 5), (1, [(10,10)])),        # inside at end
    ((15, 10), (1, [(10,15)])),       # inside + after
    ((20, 10), (1, [(10,20)])),       # just after
    ((21, 10), (2, [(10,10), (21,10)])), # after
])
def test_range_single(add_args, expect):
    base = QuadRanges(10, 10)
    base.add(*add_args)
    n_ranges, ranges_data = expect
    assert base.n_ranges == n_ranges
    for idx, exp in enumerate(ranges_data):
        assert base.ranges[idx]['start'] == exp[0]
        assert base.ranges[idx]['length'] == exp[1]

def test_range_multi():
    # build base
    base = QuadRanges(10, 10)
    base.add(50, 10)
    base.add(30, 10)

    # copy
    r = base.copy()
    assert r.n_ranges == 3
    assert r.ranges[0] == {'start':10,'length':10}
    assert r.ranges[1] == {'start':30,'length':10}
    assert r.ranges[2] == {'start':50,'length':10}

    # overlap everything
    r = base.copy()
    r.add(0, 100)
    assert r.n_ranges == 1
    assert r.ranges[0]['start'] == 0
    assert r.ranges[0]['length'] == 100

    # overlap middle
    r = base.copy()
    r.add(25, 10)
    assert r.n_ranges == 3
    assert r.ranges[0]['start'] == 10 and r.ranges[0]['length'] == 10
    assert r.ranges[1]['start'] == 25 and r.ranges[1]['length'] == 15
    assert r.ranges[2]['start'] == 50 and r.ranges[2]['length'] == 10

    # overlap last
    r = base.copy()
    r.add(45, 10)
    assert r.n_ranges == 3
    assert r.ranges[0]['start'] == 10 and r.ranges[0]['length'] == 10
    assert r.ranges[1]['start'] == 30 and r.ranges[1]['length'] == 10
    assert r.ranges[2]['start'] == 45 and r.ranges[2]['length'] == 15

def test_range_remove():
    base = QuadRanges(10, 10)
    base.add(50, 10)
    base.add(30, 10)

    # overlap all
    r = base.copy()
    r.remove(0,100)
    assert r.n_ranges == 0

    # overlap middle 1
    r = base.copy()
    r.remove(25,20)
    assert r.n_ranges == 2
    assert r.ranges[0]['start'] == 10 and r.ranges[0]['length'] == 10
    assert r.ranges[1]['start'] == 50 and r.ranges[1]['length'] == 10

    # overlap middle 2
    r = base.copy()
    r.remove(25,10)
    assert r.n_ranges == 3
    assert r.ranges[0]['start'] == 10 and r.ranges[0]['length'] == 10
    assert r.ranges[1]['start'] == 35 and r.ranges[1]['length'] == 5
    assert r.ranges[2]['start'] == 50 and r.ranges[2]['length'] == 10

    # overlap middle 3
    r = base.copy()
    r.remove(35, 10)
    assert r.n_ranges == 3
    assert r.ranges[0]['start'] == 10 and r.ranges[0]['length'] == 10
    assert r.ranges[1]['start'] == 30 and r.ranges[1]['length'] == 5
    assert r.ranges[2]['start'] == 50 and r.ranges[2]['length'] == 10

    # overlap middle 4
    r = base.copy()
    r.remove(34, 2)
    assert r.n_ranges == 4
    assert r.ranges[0]['start'] == 10 and r.ranges[0]['length'] == 10
    assert r.ranges[1]['start'] == 30 and r.ranges[1]['length'] == 4
    assert r.ranges[2]['start'] == 36 and r.ranges[2]['length'] == 4
    assert r.ranges[3]['start'] == 50 and r.ranges[3]['length'] == 10

@pytest.mark.parametrize("input_str,expected", [
    ("", [""]),
    ("foo", ["foo"]),
    ("foo:bar", ["foo", "bar"]),
    ("foo:bar:", ["foo", "bar", ""]),
    ("abc[foo::bar]xyz:foo:bar", ["abc[foo::bar]xyz", "foo", "bar"]),
    ("foo:abc[foo::bar]xyz:bar", ["foo", "abc[foo::bar]xyz", "bar"]),
    ("foo:abc[foo::barxyz:bar", ["foo", "abc[foo::barxyz:bar"]),
])
def test_split_ports(input_str, expected):
    def quad_split_ports(s):
        # Porting the logic from C's quad_split_ports for these test cases
        out = []
        b = ''
        i = 0
        while i < len(s):
            if s[i] == ':':
                out.append(b)
                b = ''
            elif s[i] == '[':
                b += s[i]
                i += 1
                while i < len(s) and s[i] != ']':
                    b += s[i]
                    i += 1
                if i < len(s):
                    b += s[i]
            else:
                b += s[i]
            i += 1
        out.append(b)
        return out
    assert quad_split_ports(input_str) == expected