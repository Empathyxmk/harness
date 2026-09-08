import pytest
from src.luautf8 import utf8

def test_pm_public():
    assert utf8.match("aéêbΓδж", ".") == "a"
    assert utf8.match("aéêbΓδж", "..") == "aé"
    assert utf8.match("aéêbΓδж", ".+") == "aéêbΓδж"
    assert utf8.match("aéêbΓδж", ".-") == ""
    assert utf8.match("aéêbΓδж", "(.)", 4) == "ê"
    assert utf8.match("aΓδжb", "(.)", -3) == "δ"

    s = "夏小今早睡了覺"
    pat = "覺"
    assert utf8.find(s, pat) == (8, 8) or utf8.find(s, pat) == 8
    assert utf8.match(s, "覺$") == "覺"
    assert utf8.gsub(s, "今", "迟")[0] == "夏小迟早睡了覺"
    assert utf8.gsub(s, "x", "Y")[1] == 0

    assert utf8.match("早安，世界！", "[世-界]") == "世"
    assert utf8.match("óэЯכוź", "[%z\1-я]") == "э"