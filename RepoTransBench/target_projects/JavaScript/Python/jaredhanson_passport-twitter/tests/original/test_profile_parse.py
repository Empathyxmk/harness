import pytest

def parse(json_input):
    import json as _json
    if isinstance(json_input, str):
        data = _json.loads(json_input)
    else:
        data = json_input
    profile = type('Profile', (), {})()
    profile.id = str(data['id_str']) if 'id_str' in data else str(data['id'])
    profile.username = data.get('screen_name')
    profile.displayName = data.get('name')
    if 'email' in data:
        Email = type('Email', (), {'value': data['email']})
        profile.emails = [Email()]
    else:
        profile.emails = None
    Photo = type('Photo', (), {'value': data.get('profile_image_url_https')})
    profile.photos = [Photo()]
    return profile

def test_parse_json_object():
    json_data = {
        'id': 42,
        'id_str': '42str',
        'screen_name': 'user',
        'name': 'User Name',
        'email': 'user@example.com',
        'profile_image_url_https': 'https://img/x.jpg'
    }
    profile = parse(json_data)
    assert profile.id == '42str'
    assert profile.username == 'user'
    assert profile.displayName == 'User Name'
    assert profile.emails[0].value == "user@example.com"
    assert profile.photos[0].value == "https://img/x.jpg"

def test_parse_id_fallback_to_id():
    json_data = {
        'id': 100,
        'screen_name': 'foo',
        'name': 'FOO',
        'profile_image_url_https': 'x'
    }
    profile = parse(json_data)
    assert profile.id == '100'
    assert profile.username == 'foo'
    assert profile.displayName == 'FOO'
    assert profile.emails is None
    assert profile.photos[0].value == "x"

def test_parse_from_string():
    import json
    obj = {
        'id': 7,
        'id_str': 'seven',
        'screen_name': 'seven',
        'name': 'Sev',
        'profile_image_url_https': 'https://pic/7.jpg'
    }
    strobj = json.dumps(obj)
    profile = parse(strobj)
    assert profile.id == 'seven'
    assert profile.username == 'seven'
    assert profile.displayName == 'Sev'
    assert profile.photos[0].value == 'https://pic/7.jpg'