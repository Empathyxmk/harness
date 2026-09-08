import pytest

class WebViewSettings:
    def __init__(self):
        self._js_enabled = True
    def get_javascript_enabled(self):
        return self._js_enabled
    def set_javascript_enabled(self, val):
        self._js_enabled = bool(val)

class WebView:
    def __init__(self):
        self.url = None
        self.settings = WebViewSettings()
    def get_settings(self):
        return self.settings
    def load_url(self, url):
        self.url = url
    def get_url(self):
        return self.url

class EditText:
    def __init__(self):
        self._text = ""
    def set_text(self, text):
        self._text = text
    def get_text(self):
        return self._text

class InputValidation2URISchemeActivity:
    def __init__(self):
        self.webview = WebView()
        self.edittext = EditText()
    def find_view_by_id(self, key):
        if key == "ivi2wview":
            return self.webview
        if key == "ivi2uri":
            return self.edittext
        if key == "issue2Input":
            return self.edittext
        return None
    def get(self, _):
        # Loads the url from edit text into webview
        url = self.edittext.get_text()
        self.webview.load_url(url)

@pytest.fixture
def activity():
    return InputValidation2URISchemeActivity()

def test_on_create_sets_layout_and_js(activity):
    wview = activity.find_view_by_id("ivi2wview")
    assert wview is not None
    assert wview.get_settings().get_javascript_enabled()

def test_get_loads_url_from_edittext(activity):
    uri = activity.find_view_by_id("ivi2uri")
    wview = activity.find_view_by_id("ivi2wview")
    uri.set_text("https://payatu.com/")
    activity.get(None)
    assert wview.get_url() == "https://payatu.com/"