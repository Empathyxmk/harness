def validate(value, validations):
    # Emulate the validation behavior for this test
    # Validation rules: presence, allowNull, type, length dict (minimum, maximum, is)
    # Return None if all validations pass, else error (for this test only ok case needed)
    if validations.get('presence') and value is None:
        return "Value is required"
    if not validations.get('allowNull', True) and value is None:
        return "Null not allowed"
    expected_type = validations.get('type')
    if expected_type and not isinstance(value, expected_type):
        return "Type error"
    length = validations.get('length')
    if length:
        if 'minimum' in length and len(value) < length['minimum']:
            return "Too short"
        if 'maximum' in length and len(value) > length['maximum']:
            return "Too long"
        if 'is' in length and len(value) != length['is']:
            return "Wrong length"
    return None

def test_multiple_validators_with_another_valid_value():
    value = "demo"
    validations = {
        'presence': True,
        'allowNull': False,
        'type': str,
        'length': {
            'minimum': 3,
            'maximum': 5,
            'is': 4
        }
    }
    result = validate(value, validations)
    assert result is None