import pytest

def async_filter(data, predicate, final_cb):
    result = []
    def next_i(i):
        if i == len(data):
            final_cb(result)
            return
        predicate(data[i], lambda keep: _filter_step(keep, i))
    def _filter_step(keep, i):
        if keep:
            result.append(data[i])
        next_i(i + 1)
    next_i(0)

def test_filter_public(capsys):
    # data: [2, 4, 6, 9, 10, 15], expected: [4, 6, 10]
    data = [2, 4, 6, 9, 10, 15]
    expected = [4, 6, 10]
    def predicate(val, cb):
        # Keep even numbers that are NOT 2
        cb((val % 2 == 0) and (val != 2))
    def final_cb(result):
        assert result == expected
        print("filter public test passed")
    async_filter(data, predicate, final_cb)
    captured = capsys.readouterr()
    assert "filter public test passed" in captured.out