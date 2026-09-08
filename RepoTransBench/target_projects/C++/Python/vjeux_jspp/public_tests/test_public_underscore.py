def test_public_underscore_sum(capsys):
    arr = [5, 9, 21]
    sum_ = 0
    for i in range(len(arr)):
        sum_ += arr[i]
    print(f"Sum: {sum_}")

    captured = capsys.readouterr()
    assert "Sum: 35" in captured.out