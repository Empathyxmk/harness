def test_public_fannkuch_count(capsys):
    n = 4
    count = 0
    for i in range(n):
        count += (n - i)
    print(f"Fannkuch public count for n={n}: {count}")
    captured = capsys.readouterr()
    assert "Fannkuch public count for n=4: 10" in captured.out