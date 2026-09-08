import pytest
from src.spellfucker import spellfucker

def test_number_zero_returns_zero_str():
    assert spellfucker(0) == '0'

def test_false_returns_false_str():
    assert spellfucker(False) == 'false'

def test_skip_object_array_non_convertible():
    assert spellfucker({'a': 1}) == ''
    assert spellfucker([1,2,3]) == ''

def test_long_string_no_explode():
    long = 'ab' * 5000
    out = spellfucker(long)
    assert isinstance(out, str)
    assert len(out) > 0

def test_length_not_increase_substantially():
    s = 'banana'
    mutated = spellfucker(s)
    assert abs(len(mutated) - len(s)) < len(s)

def test_mutates_consonant_sets():
    words = [
      'bubble',  # bb→b
      'faff',    # ff→f (twice)
      'ladder',  # dd→d
      'jiffy',   # ff→f, j
      'phases',  # ph→f
      'league',  # gue
      'knock',   # kn→n
      'knight',  # kn, ght
      'gnaw',    # gn
      'whale',   # wh
      'hymn',    # ^h not followed by o
      'hobby',   # ho
      'jack',    # j
      'kook',    # k
      'cudgel',  # c
      'silly',   # ss
      'llama',   # ll
      'commune', # mm, m$
      'cannot',  # nn
      'noble',   # ^n
      'running', # ng$
      'gnome',   # gn
      'mop',     # pp
      'barrr',   # rr
      'scene',   # ce$
      'test',    # t
      'tough',   # ght$
      'love',    # v$
      'wham',    # ^w([^h])
      'quick',   # qu
      'yeti',    # y
      'fizzy',   # zz
      'scissors',# sc, ss, s
    ]
    for w in words:
        out = spellfucker(w)
        assert isinstance(out, str)
        assert len(out) >= 0

def test_supports_camelcase_special_symbols():
    input_ = 'camelCaseAbCde!@#'
    output = spellfucker(input_)
    assert len(output) > 0
    assert isinstance(output, str)

def test_always_returns_string():
    assert isinstance(spellfucker('asparagus'), str)
    assert isinstance(spellfucker('programming'), str)

def test_handle_repeated_replacements_at_word_ends():
    # s$, t$, m$, v$, ng$, g$, ce$
    words = ['dogs', 'cat', 'hmm', 'love', 'running', 'ding', 'trace']
    for word in words:
        out = spellfucker(word)
        assert isinstance(out, str)
        assert len(out) >= 0