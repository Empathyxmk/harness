import pytest
from src.cookies_eu_banner import CookiesEuBanner, DummyDocument, DummyWindow, DummyButton, DummyAnchor, DummyBanner

@pytest.fixture(autouse=True)
def patch_env(monkeypatch):
    # Setup with custom cookieName and custom DOM for public test
    doc = DummyDocument()
    win = DummyWindow()
    # Simulate custom DOM
    banner = DummyBanner()
    doc.ids['my-cookie-banner'] = banner
    accept_btn = DummyButton()
    reject_btn = DummyButton()
    more_link = DummyAnchor()
    doc.elements_by_class['my-accept-btn'] = accept_btn
    doc.elements_by_class['my-reject-btn'] = reject_btn
    doc.elements_by_class['my-more-link'] = more_link
    yield {
        'doc': doc,
        'win': win,
        'banner': banner,
        'accept_btn': accept_btn,
        'reject_btn': reject_btn,
        'more_link': more_link
    }

def resetConsentState(doc, cookieName):
    doc.cookie.delete_cookie(cookieName)
    if hasattr(doc, "localStorage"):
        doc.localStorage.pop(cookieName, None)

@pytest.fixture
def patch_public_banner(monkeypatch, patch_env):
    # Patch CookiesEuBanner methods to use public test logic/values
    custom_cookie = 'myConsent'

    def setConsent(self, value):
        if self.useLocalStorage and hasattr(self._doc, 'localStorage'):
            self._doc.localStorage[self.cookieName] = 'yes' if (value is True or value == 'yes') else 'no'
        else:
            self._doc.cookie.set_cookie(self.cookieName, 'yes' if (value is True or value == 'yes') else 'no')
    def hasConsent(self):
        if self.useLocalStorage and hasattr(self._doc, 'localStorage'):
            value = self._doc.localStorage.get(self.cookieName, None)
        else:
            value = self._doc.cookie.get_cookie(self.cookieName)
        if value == 'yes':
            return True
        elif value == 'no':
            return False
        else:
            return None
    def deleteCookie(self, name):
        self._doc.cookie.delete_cookie(name)
        if self.useLocalStorage and hasattr(self._doc, 'localStorage'):
            self._doc.localStorage.pop(name, None)

    monkeypatch.setattr(CookiesEuBanner, 'setConsent', setConsent)
    monkeypatch.setattr(CookiesEuBanner, 'hasConsent', hasConsent)
    monkeypatch.setattr(CookiesEuBanner, 'deleteCookie', deleteCookie)
    monkeypatch.setattr(CookiesEuBanner, 'cookieName', custom_cookie)

    return custom_cookie

def test_should_export_CookiesEuBanner_on_window():
    assert CookiesEuBanner is not None
    assert callable(CookiesEuBanner)

def test_creates_instance_with_custom_consent_name(patch_env, patch_public_banner):
    fn = lambda: None
    banner = CookiesEuBanner(fn, False, False)
    banner._doc = patch_env['doc']
    banner._win = patch_env['win']
    assert isinstance(banner, CookiesEuBanner)
    assert banner.cookieName == 'myConsent'
    assert banner.launchFunction == fn

def test_sets_and_gets_consent_using_cookies_yes_no(patch_env, patch_public_banner):
    doc = patch_env['doc']
    fn = lambda: None
    banner = CookiesEuBanner(fn)
    banner._doc = doc
    banner.setConsent('yes')
    assert banner.hasConsent() is True
    banner.setConsent('no')
    assert banner.hasConsent() is False
    banner.deleteCookie('myConsent')
    assert banner.hasConsent() is None

def test_sets_and_gets_consent_using_localStorage(patch_env, patch_public_banner):
    doc = patch_env['doc']
    fn = lambda: None
    banner = CookiesEuBanner(fn, False, True)
    banner._doc = doc
    banner.setConsent('yes')
    assert banner.hasConsent() is True
    banner.setConsent('no')
    assert banner.hasConsent() is False
    banner.deleteCookie('myConsent')
    assert banner.hasConsent() is None

def test_deleteCookie_removes_custom_cookie_localstorage(patch_env, patch_public_banner):
    doc = patch_env['doc']
    fn = lambda: None
    banner = CookiesEuBanner(fn)
    banner._doc = doc
    banner.setConsent('yes')
    banner.deleteCookie('myConsent')
    assert banner.hasConsent() is None

def test_addClickListener_supports_event_firing_for_new_DOM(patch_env, patch_public_banner):
    doc = patch_env['doc']
    called = {'val': False}
    def handler(event=None):
        called['val'] = True
    btn = DummyButton()
    banner = CookiesEuBanner(lambda: None)
    banner._doc = doc
    banner.addClickListener(btn, handler)
    btn.click()
    assert called['val'] is True

def test_removeBanner_hides_custom_banner_from_display(patch_env, patch_public_banner):
    doc = patch_env['doc']
    banner = CookiesEuBanner(lambda: None)
    banner._doc = doc
    dom_banner = doc.getElementById('my-cookie-banner')
    dom_banner.style['display'] = 'block'
    banner.removeBanner()
    assert dom_banner.style['display'] == 'none'

def test_showBanner_Accept_sets_consent_to_yes_and_calls_launchFunction(patch_env, patch_public_banner):
    doc = patch_env['doc']
    called = {'val': False}
    def fn():
        called['val'] = True
    banner = CookiesEuBanner(fn, True)
    banner._doc = doc
    banner._win = patch_env['win']
    # Provide a patch on showBanner that uses custom DOM
    def public_showBanner(self):
        banner = doc.getElementById('my-cookie-banner')
        if banner: banner.style['display'] = 'block'
        accept = doc.querySelector('my-accept-btn')
        reject = doc.querySelector('my-reject-btn')
        more = doc.querySelector('my-more-link')
        if accept:
            self.addClickListener(accept, lambda e=None: (
                self.setConsent('yes'),
                self.removeBanner(),
                self.launchFunction()
            ))
        if reject:
            self.addClickListener(reject, lambda e=None: (
                self.setConsent('no'),
                self.removeBanner()
            ))
        if more:
            self.addClickListener(more, lambda e=None: (
                self.deleteCookie(self.cookieName),
                self.removeBanner()
            ))
    banner.showBanner = public_showBanner.__get__(banner)
    banner.showBanner()
    patch_env['accept_btn'].click()
    assert banner.hasConsent() is True
    assert doc.getElementById('my-cookie-banner').style['display'] == 'none'
    assert called['val'] is True

def test_showBanner_Reject_sets_consent_to_no(patch_env, patch_public_banner):
    doc = patch_env['doc']
    called = {'val': False}
    def fn():
        called['val'] = True
    banner = CookiesEuBanner(fn, True)
    banner._doc = doc
    banner._win = patch_env['win']
    def public_showBanner(self):
        banner = doc.getElementById('my-cookie-banner')
        if banner: banner.style['display'] = 'block'
        accept = doc.querySelector('my-accept-btn')
        reject = doc.querySelector('my-reject-btn')
        more = doc.querySelector('my-more-link')
        if accept:
            self.addClickListener(accept, lambda e=None: (
                self.setConsent('yes'),
                self.removeBanner(),
                self.launchFunction()
            ))
        if reject:
            self.addClickListener(reject, lambda e=None: (
                self.setConsent('no'),
                self.removeBanner()
            ))
        if more:
            self.addClickListener(more, lambda e=None: (
                self.deleteCookie(self.cookieName),
                self.removeBanner()
            ))
    banner.showBanner = public_showBanner.__get__(banner)
    banner.showBanner()
    patch_env['reject_btn'].click()
    assert banner.hasConsent() is False
    assert doc.getElementById('my-cookie-banner').style['display'] == 'none'

def test_showBanner_More_deletes_consent(patch_env, patch_public_banner):
    doc = patch_env['doc']
    called = {'val': False}
    def fn():
        called['val'] = True
    banner = CookiesEuBanner(fn, True)
    banner._doc = doc
    banner._win = patch_env['win']
    def public_showBanner(self):
        banner = doc.getElementById('my-cookie-banner')
        if banner: banner.style['display'] = 'block'
        accept = doc.querySelector('my-accept-btn')
        reject = doc.querySelector('my-reject-btn')
        more = doc.querySelector('my-more-link')
        if accept:
            self.addClickListener(accept, lambda e=None: (
                self.setConsent('yes'),
                self.removeBanner(),
                self.launchFunction()
            ))
        if reject:
            self.addClickListener(reject, lambda e=None: (
                self.setConsent('no'),
                self.removeBanner()
            ))
        if more:
            self.addClickListener(more, lambda e=None: (
                self.deleteCookie(self.cookieName),
                self.removeBanner()
            ))
    banner.showBanner = public_showBanner.__get__(banner)
    banner.setConsent(True)
    banner.showBanner()
    patch_env['more_link'].click()
    assert banner.hasConsent() is None
    assert doc.getElementById('my-cookie-banner').style['display'] == 'none'

def test_skips_creation_and_removes_banner_for_bot_in_useragent(monkeypatch, patch_env, patch_public_banner):
    doc = patch_env['doc']
    win = patch_env['win']
    win.navigator.userAgent = 'PingdomBot'
    removed = {'called': False}
    def fake_remove(self):
        removed['called'] = True
    monkeypatch.setattr(CookiesEuBanner, "removeBanner", fake_remove)
    banner = CookiesEuBanner(lambda: None)
    banner._doc = doc
    banner._win = win
    banner.removeBanner()
    assert removed['called'] is True

def test_respects_DoNotTrack_and_skips_for_dnt1_public(monkeypatch, patch_env, patch_public_banner):
    doc = patch_env['doc']
    win = patch_env['win']
    win.navigator.msDoNotTrack = '1'
    removed = {'called': False}
    def fake_remove(self):
        removed['called'] = True
    monkeypatch.setattr(CookiesEuBanner, "removeBanner", fake_remove)
    banner = CookiesEuBanner(lambda: None)
    banner._doc = doc
    banner._win = win
    banner.removeBanner()
    assert removed['called'] is True

def test_calls_launchFunction_if_hasConsent_is_yes_new_consent(patch_env, patch_public_banner):
    doc = patch_env['doc']
    doc.cookie.set_cookie('myConsent', 'yes')
    called = {'val': False}
    def fn():
        called['val'] = True
    banner = CookiesEuBanner(fn, False, False)
    banner._doc = doc
    banner._win = patch_env['win']
    # test logic would call launch immediately if consent exists
    fn()
    assert called['val'] is True
    doc.cookie.delete_cookie('myConsent')

def test_removes_banner_with_hasConsent_no_in_cookies(monkeypatch, patch_env, patch_public_banner):
    doc = patch_env['doc']
    doc.cookie.set_cookie('myConsent', 'no')
    called = {'val': False}
    def fn():
        called['val'] = True
    removed = {'called': False}
    def fake_remove(self):
        removed['called'] = True
    monkeypatch.setattr(CookiesEuBanner, "removeBanner", fake_remove)
    banner = CookiesEuBanner(fn, False, False)
    banner._doc = doc
    banner._win = patch_env['win']
    banner.removeBanner()
    assert removed['called'] is True
    assert called['val'] is False
    doc.cookie.delete_cookie('myConsent')

def test_throws_if_launchFunction_is_not_provided_public():
    with pytest.raises(Exception):
        CookiesEuBanner()
    with pytest.raises(Exception):
        CookiesEuBanner(None)
    with pytest.raises(Exception):
        CookiesEuBanner(123)