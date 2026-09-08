from pytracking import (
    Configuration, TRACKING_PIXEL, PNG_MIME_TYPE, DEFAULT_TIMEOUT_SECONDS
)
from pytracking import (
    get_click_tracking_url, get_click_tracking_result, get_open_tracking_result,
    get_open_tracking_url, get_open_tracking_url_path,
    get_click_tracking_url_path, get_open_tracking_pixel,
)

def test_public_init_exports_access():
    assert isinstance(Configuration(), Configuration)
    assert isinstance(TRACKING_PIXEL, bytes)
    assert isinstance(PNG_MIME_TYPE, str)
    assert isinstance(DEFAULT_TIMEOUT_SECONDS, int)
    # Test callable exported functions
    assert callable(get_click_tracking_url)
    assert callable(get_click_tracking_result)
    assert callable(get_open_tracking_result)
    assert callable(get_open_tracking_url)
    assert callable(get_open_tracking_url_path)
    assert callable(get_click_tracking_url_path)
    assert callable(get_open_tracking_pixel)