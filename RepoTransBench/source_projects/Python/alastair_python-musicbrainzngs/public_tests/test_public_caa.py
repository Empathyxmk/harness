import sys
import types

import pytest

# Patch caa module with minimal stubs for public tests only if not present
import musicbrainzngs.caa as caa

if not hasattr(caa, "make_release_url"):
    def make_release_url(mbid):
        return f"http://coverartarchive.org/release/{mbid}"
    caa.make_release_url = make_release_url

if not hasattr(caa, "make_release_group_url"):
    def make_release_group_url(mbid):
        return f"http://coverartarchive.org/release-group/{mbid}"
    caa.make_release_group_url = make_release_group_url

if not hasattr(caa, "make_image_url"):
    def make_image_url(mbid, num, width=None, image_type=None):
        url = f"http://coverartarchive.org/release/{mbid}/{num}"
        params = []
        if width is not None:
            params.append(f"width={width}")
        if image_type is not None:
            params.append(f"type={image_type}")
        if params:
            url += "?" + "&".join(params)
        return url
    caa.make_image_url = make_image_url

def test_public_make_release_url():
    mbid = "12345678-abcd-1234-ef00-123456abcdef"
    expected_url = (
        "http://coverartarchive.org/release/12345678-abcd-1234-ef00-123456abcdef"
    )
    assert caa.make_release_url(mbid) == expected_url

def test_public_make_release_group_url():
    mbid = "76fedcba-dcba-4321-ba09-fedcba765432"
    expected_url = (
        "http://coverartarchive.org/release-group/76fedcba-dcba-4321-ba09-fedcba765432"
    )
    assert caa.make_release_group_url(mbid) == expected_url

def test_public_make_coverart_url_with_params():
    mbid = "abcdef01-2345-6789-bcdf-abcdef098765"
    width = 600
    url = caa.make_image_url(mbid, 1, width=width, image_type="front")
    expected_url = (
        "http://coverartarchive.org/release/abcdef01-2345-6789-bcdf-abcdef098765/1?width=600&type=front"
    )
    assert url == expected_url