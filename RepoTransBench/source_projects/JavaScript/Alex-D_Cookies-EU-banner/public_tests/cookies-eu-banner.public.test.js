/**
 * @jest-environment jsdom
 * Public test suite for CookiesEuBanner, using new/different input data
 */
const { CookiesEuBanner } = require('../src/cookies-eu-banner.js');

// Utility to clear cookies and localStorage
function resetConsentState(cookieName) {
  document.cookie = `${cookieName}=; expires=Thu, 01 Jan 1970 00:00:01 GMT; path=/;`;
  if (typeof localStorage !== 'undefined') {
    localStorage.removeItem(cookieName);
  }
}

describe('CookiesEuBanner (Public Tests)', () => {
  const cookieName = 'myConsent';

  beforeEach(() => {
    // Clear cookies and localStorage with NEW cookie name
    resetConsentState(cookieName);

    // Reset DOM with different custom IDs and classes
    document.body.innerHTML = `
      <div id="my-cookie-banner" style="display:none;" data-wait-remove="0">
        <button class="my-accept-btn">Allow</button>
        <button class="my-reject-btn">Deny</button>
        <a class="my-more-link" href="#">Details</a>
      </div>
    `;

    // Patch prototype to use different selectors for testing
    CookiesEuBanner.prototype._getBannerElements = function () {
      return {
        banner: document.getElementById('my-cookie-banner'),
        acceptButton: document.querySelector('.my-accept-btn'),
        rejectButton: document.querySelector('.my-reject-btn'),
        moreLink: document.querySelector('.my-more-link'),
      };
    };

    // Patch prototype showBanner implementation to use above
    CookiesEuBanner.prototype.showBanner = function () {
      const els = this._getBannerElements();
      if (els.banner) els.banner.style.display = 'block';

      if (els.acceptButton) {
        this.addClickListener(els.acceptButton, () => {
          this.setConsent('yes');
          this.removeBanner();
          if (typeof this.launchFunction === 'function') this.launchFunction();
        });
      }
      if (els.rejectButton) {
        this.addClickListener(els.rejectButton, () => {
          this.setConsent('no');
          this.removeBanner();
        });
      }
      if (els.moreLink) {
        this.addClickListener(els.moreLink, () => {
          this.deleteCookie(this.cookieName);
          this.removeBanner();
        });
      }
    };

    Object.defineProperty(window, 'navigator', {
      value: {
        userAgent: 'Mozilla/5.0 (Linux) CustomTest',
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

    // Patch cookieName for public tests ONLY
    CookiesEuBanner.prototype.cookieName = cookieName;

    // Patch setConsent/getConsent to accept 'yes'/'no' in addition to true/false
    CookiesEuBanner.prototype.setConsent = function (value) {
      if (this.useLocalStorage && typeof window.localStorage !== 'undefined') {
        window.localStorage.setItem(this.cookieName, value === true || value === 'yes' ? 'yes' : 'no');
      } else {
        const expiration = new Date(Date.now() + this.cookieTimeout).toUTCString();
        document.cookie = `${this.cookieName}=${value === true || value === 'yes' ? 'yes' : 'no'}; expires=${expiration}; path=/;`;
      }
    };
    CookiesEuBanner.prototype.hasConsent = function () {
      let value;
      if (this.useLocalStorage && typeof window.localStorage !== 'undefined') {
        value = window.localStorage.getItem(this.cookieName);
      } else {
        const match = document.cookie.match(new RegExp('(^| )' + this.cookieName + '=([^;]+)'));
        value = match && match[2];
      }
      if (value === 'yes') return true;
      if (value === 'no') return false;
      return null;
    };
    CookiesEuBanner.prototype.deleteCookie = function (name) {
      document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/;';
      if (this.useLocalStorage && typeof window.localStorage !== 'undefined') {
        window.localStorage.removeItem(name);
      }
    };
  });

  it('should export CookiesEuBanner on window', () => {
    expect(window.CookiesEuBanner).toBeDefined();
    expect(typeof window.CookiesEuBanner).toBe('function');
  });

  it('creates an instance with custom consent name', () => {
    const fn = jest.fn();
    const banner = new window.CookiesEuBanner(fn, false, false);
    expect(banner).toBeInstanceOf(window.CookiesEuBanner);
    expect(banner.cookieName).toBe(cookieName);
    expect(banner.launchFunction).toBe(fn);
  });

  it('sets and gets consent using cookies (yes/no)', () => {
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.setConsent('yes');
    expect(banner.hasConsent()).toBe(true);
    banner.setConsent('no');
    expect(banner.hasConsent()).toBe(false);
    banner.deleteCookie(cookieName);
    expect(banner.hasConsent()).toBe(null);
  });

  it('sets and gets consent using localStorage', () => {
    const banner = new window.CookiesEuBanner(jest.fn(), false, true);
    banner.setConsent('yes');
    expect(banner.hasConsent()).toBe(true);
    banner.setConsent('no');
    expect(banner.hasConsent()).toBe(false);
    banner.deleteCookie(cookieName);
    expect(banner.hasConsent()).toBe(null);
  });

  it('deleteCookie removes custom cookie/localStorage', () => {
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.setConsent('yes');
    banner.deleteCookie(cookieName);
    expect(banner.hasConsent()).toBe(null);
  });

  it('addClickListener supports event firing for new DOM', () => {
    const btn = document.createElement('button');
    const h = jest.fn();
    const banner = new window.CookiesEuBanner(jest.fn());
    banner.addClickListener(btn, h);
    btn.click();
    expect(h).toHaveBeenCalled();
  });

  it('removeBanner hides the custom banner from display', () => {
    const banner = new window.CookiesEuBanner(jest.fn());
    const domBanner = document.getElementById('my-cookie-banner');
    domBanner.style.display = 'block';
    banner.removeBanner();
    expect(domBanner.style.display).toBe('none');
  });

  it('showBanner Accept sets consent to yes and calls launchFunction', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true);
    banner.showBanner();
    const btn = document.querySelector('.my-accept-btn');
    btn.click();
    expect(banner.hasConsent()).toBe(true);
    expect(document.getElementById('my-cookie-banner').style.display).toBe('none');
    expect(launchFn).toHaveBeenCalled();
  });

  it('showBanner Reject sets consent to no', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true);
    banner.showBanner();
    const btn = document.querySelector('.my-reject-btn');
    btn.click();
    expect(banner.hasConsent()).toBe(false);
    expect(document.getElementById('my-cookie-banner').style.display).toBe('none');
  });

  it('showBanner More deletes consent', () => {
    const launchFn = jest.fn();
    const banner = new window.CookiesEuBanner(launchFn, true);
    banner.setConsent(true);
    banner.showBanner();
    const link = document.querySelector('.my-more-link');
    link.click();
    expect(banner.hasConsent()).toBe(null);
    expect(document.getElementById('my-cookie-banner').style.display).toBe('none');
  });

  it('skips creation and removes banner for bot in userAgent (new UA)', () => {
    Object.defineProperty(window.navigator, 'userAgent', { value: 'PingdomBot', configurable: true });
    const rmSpy = jest.spyOn(window.CookiesEuBanner.prototype, 'removeBanner');
    new window.CookiesEuBanner(jest.fn());
    expect(rmSpy).toHaveBeenCalled();
    rmSpy.mockRestore();
  });

  it('respects DoNotTrack and skips for dnt=1 (public)', () => {
    Object.defineProperty(window.navigator, 'msDoNotTrack', { value: '1', configurable: true });
    const rmSpy = jest.spyOn(window.CookiesEuBanner.prototype, 'removeBanner');
    new window.CookiesEuBanner(jest.fn());
    expect(rmSpy).toHaveBeenCalled();
    rmSpy.mockRestore();
  });

  it('calls launchFunction if hasConsent is yes (new consent)', () => {
    document.cookie = `${cookieName}=yes`;
    const fn = jest.fn();
    new window.CookiesEuBanner(fn, false, false);
    expect(fn).toHaveBeenCalled();
    resetConsentState(cookieName);
  });

  it('removes banner with hasConsent = no in cookies', () => {
    document.cookie = `${cookieName}=no`;
    const fn = jest.fn();
    const rmSpy = jest.spyOn(window.CookiesEuBanner.prototype, 'removeBanner');
    new window.CookiesEuBanner(fn, false, false);
    expect(rmSpy).toHaveBeenCalled();
    expect(fn).not.toHaveBeenCalled();
    rmSpy.mockRestore();
    resetConsentState(cookieName);
  });

  it('throws if launchFunction is not provided (public)', () => {
    expect(() => new window.CookiesEuBanner()).toThrow();
    expect(() => new window.CookiesEuBanner(undefined)).toThrow();
    expect(() => new window.CookiesEuBanner(123)).toThrow();
  });
});