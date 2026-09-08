from src.PropTypes import PropTypes, config_style_validator

def check_type(props):
    try:
        PropTypes.style(props['style'])
        return False  # If no error, then not a type error
    except Exception:
        return True

def test_does_not_error_for_valid_style():
    config_style_validator({"strict": False, "warn": False})
    assert not check_type({"style": {"backgroundColor": "red"}})