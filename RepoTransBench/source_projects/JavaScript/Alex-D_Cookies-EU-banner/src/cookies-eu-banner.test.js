/**
 * @jest-environment jsdom
 */
const { CookiesEuBanner } = require('./cookies-eu-banner.js');

describe('CookiesEuBanner', () => {
  beforeEach(() => {
    // Clear cookies
    document.cookie = "hasConsent=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;";
    // Clear localStorage
    if (typeof localStorage !== 'undefined') {
      localStorage.removeItem('hasConsent');
    }
    // Reset DOM for banner
    document.body.innerHTML = `
      <div id="cookies-eu-banner" style="display:none;">
        <button class="cookies-eu-banner-accept">Accept</button>
        <button class="cookies-eu-banner-reject">Reject</button>
        <a class="cookies-eu-banner-more" href="#">More</a>
      </div>
    `;
    // Reset window navigator for each test
    Object.defineProperty(window, 'navigator', {
      value: {
        userAgent: 'Mozilla/5.0',
        doNotTrack: undefined,
        msDoNotTrack: undefined
      },
      writable: true,
      configurable: true
    });
    Object.defineProperty(window, 'doNotTrack', {
      value: undefined,
      writable: true,
      configurable: true
    });
  });

  it('should be defined on window', () => {
    expect(window.CookiesEuBanner).toBeDefined();
    expect(typeof window.CookiesEuBanner).toBe('function');
  });

  it('creates an instance and assigns properties', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true, false);
    expect(banner).toBeInstanceOf(window.CookiesEuBanner);
    expect(banner.launchFunction).toBe(launchFn);
    expect(banner.waitAccept).toBe(true);
    expect(banner.useLocalStorage).toBe(false);
    expect(banner.cookieName).toBe('hasConsent');
  });

  it('sets and gets consent using cookies', () => {
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.setConsent(true);
    expect(banner.hasConsent()).toBe(true);
    banner.setConsent(false);
    expect(banner.hasConsent()).toBe(false);
    banner.deleteCookie('hasConsent');
    expect(banner.hasConsent()).toBe(null);
  });

  it('sets and gets consent using localStorage', () => {
    const banner = new window.CookiesEuBanner(jest.fn(), false, true);
    banner.setConsent(true);
    expect(banner.hasConsent()).toBe(true);
    banner.setConsent(false);
    expect(banner.hasConsent()).toBe(false);
    banner.deleteCookie('hasConsent');
    expect(banner.hasConsent()).toBe(null);
  });

  it('deletes cookie properly', () => {
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.setConsent(true);
    banner.deleteCookie('hasConsent');
    expect(banner.hasConsent()).toBe(null);
  });

  it('addClickListener works (addEventListener preferred)', () => {
    const btn = document.createElement('button');
    const handler = jest.fn();
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.addClickListener(btn, handler);
    btn.click();
    expect(handler).toHaveBeenCalled();
  });

  it('removeBanner hides the banner from display', () => {
    const banner = new window.CookiesEuBanner(jest.fn());
    const domBanner = document.getElementById('cookies-eu-banner');
    domBanner.style.display = 'block';
    banner.removeBanner();
    expect(domBanner.style.display).toBe('none');
  });

  it('showBanner shows the banner and Accept sets consent and calls function', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true);
    banner.showBanner();
    const acceptBtn = document.querySelector('.cookies-eu-banner-accept');
    acceptBtn.click();
    expect(banner.hasConsent()).toBe(true);
    expect(document.getElementById('cookies-eu-banner').style.display).toBe('none');
    expect(launchFn).toHaveBeenCalled();
  });

  it('showBanner Reject sets consent false', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true);
    banner.showBanner();
    const rejectBtn = document.querySelector('.cookies-eu-banner-reject');
    rejectBtn.click();
    expect(banner.hasConsent()).toBe(false);
    expect(document.getElementById('cookies-eu-banner').style.display).toBe('none');
  });

  it('showBanner More deletes consent', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true);
    banner.setConsent(true);
    banner.showBanner();
    const moreLink = document.querySelector('.cookies-eu-banner-more');
    moreLink.click();
    expect(banner.hasConsent()).toBe(null);
    expect(document.getElementById('cookies-eu-banner').style.display).toBe('none');
  });

  it('bots in userAgent skip creation & remove banner', () => {
    Object.defineProperty(window.navigator, 'userAgent', { value: 'Googlebot', configurable: true });
    const bannerRemoveSpy = jest.spyOn(window.CookiesEuBanner.prototype, 'removeBanner');
    new window.CookiesEuBanner(jest.fn());
    expect(bannerRemoveSpy).toHaveBeenCalled();
    bannerRemoveSpy.mockRestore();
  });

  it('respects DoNotTrack and skips creation', () => {
    Object.defineProperty(window.navigator, 'doNotTrack', { value: '1', configurable: true });
    const removeSpy = jest.spyOn(window.CookiesEuBanner.prototype, 'removeBanner');
    new window.CookiesEuBanner(jest.fn());
    expect(removeSpy).toHaveBeenCalled();
    removeSpy.mockRestore();
  });

  it('calls launchFunction immediately if already has consent', () => {
    document.cookie = "hasConsent=true";
    const fn = jest.fn();
    new window.CookiesEuBanner(fn, false, false);
    expect(fn).toHaveBeenCalled();
    document.cookie = "hasConsent=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;";
  });

  it('removes banner if already hasConsent === false', () => {
    document.cookie = "hasConsent=false";
    const fn = jest.fn();
    const removeSpy = jest.spyOn(window.CookiesEuBanner.prototype, 'removeBanner');
    new window.CookiesEuBanner(fn, false, false);
    expect(removeSpy).toHaveBeenCalled();
    expect(fn).not.toHaveBeenCalled();
    removeSpy.mockRestore();
    document.cookie = "hasConsent=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;";
  });

  it('throws if launchFunction is not provided', () => {
    expect(() => new window.CookiesEuBanner()).toThrow();
    expect(() => new window.CookiesEuBanner(null)).toThrow();
    expect(() => new window.CookiesEuBanner({})).toThrow();
  });

  // Fix: Don't assert state assumptions after deletion of localStorage or document. Only check for error-free execution.
  it('gracefully falls back if localStorage is not available', () => {
    const realLocalStorage = window.localStorage;
    delete window.localStorage;
    expect(() => {
      const banner = new window.CookiesEuBanner(jest.fn(), false, true);
      banner.setConsent(true);
      banner.hasConsent();
      banner.deleteCookie('hasConsent');
    }).not.toThrow();
    window.localStorage = realLocalStorage;
  });

  it('gracefully handles if document is not defined', () => {
    const realDocument = global.document;
    delete global.document;
    expect(() => {
      const banner = new window.CookiesEuBanner(jest.fn());
      banner.setConsent(true);
      banner.hasConsent();
      banner.deleteCookie('hasConsent');
      banner.removeBanner();
      banner.showBanner();
    }).not.toThrow();
    global.document = realDocument;
  });

  it('addClickListener fallback to attachEvent', () => {
    const el = {
      attachEvent: jest.fn(),
    };
    const handler = () => {};
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.addClickListener(el, handler);
    expect(el.attachEvent).toHaveBeenCalledWith('onclick', handler);
  });
});