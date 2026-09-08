import pytest

def async_whilst(condition, iteration, done):
    def loop():
        if not condition():
            done(None)
            return
        iteration(lambda err: loop())
    loop()

def test_whilst_public(capsys):
    counter = [1]
    sum_result = [0]
    def condition():
        return counter[0] <= 3
    def iteration(next_fn):
        sum_result[0] += counter[0] * 2
        counter[0] += 1
        next_fn(None)
    def done(err):
        assert sum_result[0] == 12
        print("whilst public test passed")
    async_whilst(condition, iteration, done)
    captured = capsys.readouterr()
    assert "whilst public test passed" in captured.out