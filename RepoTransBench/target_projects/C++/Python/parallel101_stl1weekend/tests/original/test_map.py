def test_map_basic():
    table = {}
    table["delay"] = 12
    if "delay" not in table:
        table["delay"] = 32
    table["timeout"] = 42

    printed = []
    for k, v in table.items():
        printed.append(f"{k}={v}")
    # Basic check
    assert "delay=12" in printed and "timeout=42" in printed
    # at(delay)
    delay_val = table["delay"]
    assert delay_val == 12
    # size
    assert len(table) == 2