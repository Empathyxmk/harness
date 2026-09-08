from pytracking import (
    Configuration, get_click_tracking_url, get_click_tracking_url_path,
    get_open_tracking_url_path,
    get_click_tracking_result, get_open_tracking_pixel, get_open_tracking_url,
    get_open_tracking_result)

ALT_URL_TO_TRACK = "https://anotherdomain.io/tracking/?data=newdata"

ALT_BASE_CLICK_TRACKING_URL = "https://y.z.com/track/"

ALT_BASE_OPEN_TRACKING_URL = "https://y.z.com/track/open/"

ALT_ENCRYPTION_KEY = b'KJhVbRLnoCIPBLB7UfPIW3vOTsmUNxCZ-2inOtTdu6UV='

ALT_METADATA = {
    "param4": "val4",
    "another": True,
    "nested_alt": {"paramA": "valA"}}

ALT_DEFAULT_METADATA = {
    "key42": False,
    "strangeé": "winoèèè",
    "paramX": "other3"
}

ALT_EXPECTED_METADATA = {}
ALT_EXPECTED_METADATA.update(ALT_DEFAULT_METADATA)
ALT_EXPECTED_METADATA.update(ALT_METADATA)

ALT_WEBHOOK_URL = "https://notify.me/webhook/"

ALT_REQUEST_DATA = {
    "user_agent": "Safari",
    "user_ip": "192.168.1.1"
}

ALT_CONFIGURATION = Configuration(
    webhook_url=ALT_WEBHOOK_URL,
    base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL,
    base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL,
    default_metadata=ALT_DEFAULT_METADATA)

def test_public_get_open_tracking_pixel():
    (pixel, mime) = get_open_tracking_pixel()
    assert isinstance(pixel, bytes)
    assert mime == "image/png"

def test_public_basic_get_open_tracking_url():
    url = get_open_tracking_url(
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL)
    assert url.startswith(ALT_BASE_OPEN_TRACKING_URL)
    assert url[len(ALT_BASE_OPEN_TRACKING_URL):] != ""  # ensure there's something encoded

def test_public_basic_get_open_tracking_url_append_slash():
    url = get_open_tracking_url(
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL,
        append_slash=True)
    assert url.endswith("/")

def test_public_in_config_open_tracking_url():
    url = get_open_tracking_url(
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL,
        metadata=ALT_METADATA)
    path = get_open_tracking_url_path(
        url, base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL)

    tracking_result = get_open_tracking_result(
        path, webhook_url=ALT_WEBHOOK_URL)
    assert tracking_result.tracked_url is None
    assert tracking_result.webhook_url == ALT_WEBHOOK_URL
    assert tracking_result.request_data is None
    assert tracking_result.metadata == ALT_METADATA
    assert tracking_result.is_open_tracking
    assert not tracking_result.is_click_tracking

def test_public_in_config_open_tracking_url_to_json():
    url = get_open_tracking_url(
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL,
        metadata=ALT_METADATA)
    path = get_open_tracking_url_path(
        url, base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL)

    tracking_result = get_open_tracking_result(
        path, webhook_url=ALT_WEBHOOK_URL).to_json_dict()
    assert tracking_result.tracked_url is None
    assert tracking_result.webhook_url == ALT_WEBHOOK_URL
    assert tracking_result.request_data is None
    assert tracking_result.metadata == ALT_METADATA
    assert tracking_result.is_open_tracking
    assert not tracking_result.is_click_tracking

def test_public_in_config_open_tracking_full_url():
    url = get_open_tracking_url(
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL,
        metadata=ALT_METADATA)

    tracking_result = get_open_tracking_result(
        url, webhook_url=ALT_WEBHOOK_URL,
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL)

    assert tracking_result.tracked_url is None
    assert tracking_result.webhook_url == ALT_WEBHOOK_URL
    assert tracking_result.request_data is None
    assert tracking_result.metadata == ALT_METADATA
    assert tracking_result.is_open_tracking
    assert not tracking_result.is_click_tracking

def test_public_embedded_open_tracking_url():
    url = get_open_tracking_url(
        base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL,
        webhook_url=ALT_WEBHOOK_URL,
        include_webhook_url=True,
        default_metadata=ALT_DEFAULT_METADATA,
        include_default_metadata=True,
        metadata=ALT_METADATA)
    path = get_open_tracking_url_path(
        url, base_open_tracking_url=ALT_BASE_OPEN_TRACKING_URL)

    tracking_result = get_open_tracking_result(
        path, request_data=ALT_REQUEST_DATA,
        include_default_metadata=True,
        include_webhook_url=True)

    assert tracking_result.tracked_url is None
    assert tracking_result.webhook_url == ALT_WEBHOOK_URL
    assert tracking_result.request_data == ALT_REQUEST_DATA
    assert tracking_result.metadata == ALT_EXPECTED_METADATA
    assert tracking_result.is_open_tracking
    assert not tracking_result.is_click_tracking

def test_public_basic_get_click_tracking_url():
    url = get_click_tracking_url(
        ALT_URL_TO_TRACK,
        base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL)
    assert url.startswith(ALT_BASE_CLICK_TRACKING_URL)
    assert "=" in url

def test_public_basic_get_click_tracking_url_append_slash():
    url = get_click_tracking_url(
        ALT_URL_TO_TRACK,
        base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL,
        append_slash=True)
    assert url.endswith("/")

def test_public_in_config_click_tracking_url():
    url = get_click_tracking_url(
        ALT_URL_TO_TRACK,
        base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL,
        metadata=ALT_METADATA)
    path = get_click_tracking_url_path(
        url, base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL)

    tracking_result = get_click_tracking_result(
        path, webhook_url=ALT_WEBHOOK_URL)
    assert tracking_result.tracked_url == ALT_URL_TO_TRACK
    assert tracking_result.webhook_url == ALT_WEBHOOK_URL
    assert tracking_result.request_data is None
    assert tracking_result.metadata == ALT_METADATA
    assert tracking_result.is_click_tracking
    assert not tracking_result.is_open_tracking

def test_public_in_config_click_tracking_full_url():
    url = get_click_tracking_url(
        ALT_URL_TO_TRACK,
        base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL,
        metadata=ALT_METADATA)

    tracking_result = get_click_tracking_result(
        url,
        webhook_url=ALT_WEBHOOK_URL,
        base_click_tracking_url=ALT_BASE_CLICK_TRACKING_URL)

    assert tracking_result.tracked_url == ALT_URL_TO_TRACK
    assert tracking_result.webhook_url == ALT_WEBHOOK_URL
    assert tracking_result.request_data is None
    assert tracking_result.metadata == ALT_METADATA
    assert tracking_result.is_click_tracking
    assert not tracking_result.is_open_tracking