def is_default_modifier(modifiers):
    if any(m in modifiers for m in [1, 2, 3]):  # PRIVATE, PROTECTED, PUBLIC
        return False
    return True

def test_is_default_modifier():
    # Map to Modifier.{PUBLIC:3,PRIVATE:1,PROTECTED:2,FINAL:4,STATIC:5}
    PUBLIC = 3
    PRIVATE = 1
    PROTECTED = 2
    FINAL = 4
    STATIC = 5

    modifiers = set([PUBLIC])
    assert is_default_modifier(modifiers) is False

    modifiers = set([PRIVATE])
    assert is_default_modifier(modifiers) is False

    modifiers = set([PROTECTED])
    assert is_default_modifier(modifiers) is False

    modifiers = set([FINAL, STATIC])
    assert is_default_modifier(modifiers) is True