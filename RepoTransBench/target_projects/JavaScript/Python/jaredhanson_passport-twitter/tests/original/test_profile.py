import pytest
import json
import os

def load_fixture(path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

class Profile:
    def __init__(self, json_obj):
        self.id = str(json_obj.get('id_str', json_obj.get('id', '')))
        self.username = json_obj.get('screen_name')
        self.displayName = json_obj.get('name')
        self.photos = []
        if 'profile_image_url_https' in json_obj:
            self.photos.append({'value': json_obj['profile_image_url_https']})
        self.provider = 'twitter'

def test_profile_parsing_with_id_str():
    # Equivalent to test using test/fixtures/users/rsarver.json
    filename = os.path.join('tests', 'original', 'fixtures', 'users', 'rsarver.json')
    js = load_fixture(filename)
    profile = Profile(js)
    assert profile.provider == "twitter"
    assert profile.id == "795548"
    assert profile.username == "rsarver"
    assert profile.displayName == "Ryan Sarver"
    assert isinstance(profile.photos, list)
    assert profile.photos[0]['value'] == js['profile_image_url_https']

def test_profile_parsing_without_id_str():
    # Equivalent to test using test/fixtures/users/rsarver-without-id_str.json
    filename = os.path.join('tests', 'original', 'fixtures', 'users', 'rsarver-without-id_str.json')
    js = load_fixture(filename)
    profile = Profile(js)
    assert profile.provider == "twitter"
    assert profile.id == str(js['id'])  # fallback to numeric ID if id_str missing
    assert profile.username == "rsarver"
    assert profile.displayName == "Ryan Sarver"
    assert isinstance(profile.photos, list)
    assert profile.photos[0]['value'] == js['profile_image_url_https']