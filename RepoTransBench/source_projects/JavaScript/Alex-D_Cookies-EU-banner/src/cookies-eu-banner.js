/*!
 * cookies-eu-banner v2.0.1 | MIT License
 * Copyright (C) 2014-2019 Alex-D
 * https://github.com/Alex-D/Cookies-EU-banner
 * Slightly adjusted for Node/jest testability.
*/

(function(root, factory) {
    // Expose to both browser global (window) and node (global)
    if (typeof module === 'object' && module.exports) {
        module.exports = factory();
        if (typeof window !== 'undefined') {
            window.CookiesEuBanner = module.exports;
        }
        if (typeof global !== 'undefined') {
            global.CookiesEuBanner = module.exports;
        }
    } else {
        root.CookiesEuBanner = factory();
    }
}(typeof self !== 'undefined' ? self : this, function() {
    "use strict";

    function isBot(userAgent) {
        return /(bot|crawler|spider|crawling)/i.test(userAgent);
    }

    function CookiesEuBanner(launchFunction, waitAccept, useLocalStorage) {
        if (!launchFunction || typeof launchFunction !== 'function') {
            throw new Error('CookiesEuBanner: launchFunction argument is required and must be a function');
        }
        this.launchFunction = launchFunction;
        this.waitAccept = !!waitAccept;
        this.useLocalStorage = !!useLocalStorage;
        this.cookieName = 'hasConsent';
        this.bannerId = 'cookies-eu-banner';
        this.acceptBtnClass = 'cookies-eu-banner-accept';
        this.rejectBtnClass = 'cookies-eu-banner-reject';
        this.moreBtnClass = 'cookies-eu-banner-more';

        // Detect bots
        var userAgent = (typeof navigator !== 'undefined' && navigator.userAgent) || '';
        if (isBot(userAgent)) {
            this.removeBanner();
            return;
        }
        // Respect DoNotTrack
        var dnt = (typeof navigator !== 'undefined') &&
            (navigator.doNotTrack === '1' || navigator.doNotTrack === 'yes' || navigator.msDoNotTrack === '1' || window.doNotTrack === '1');
        if (dnt) {
            this.removeBanner();
            return;
        }

        // Consent already granted/denied
        var consent = this.hasConsent();
        if (consent === true) {
            this.removeBanner();
            this.launchFunction();
            return;
        } else if (consent === false) {
            this.removeBanner();
            return;
        }

        // Show banner, wait for accept
        if (!this.waitAccept) {
            this.launchFunction();
        }
        this.showBanner();
    }

    CookiesEuBanner.prototype.setConsent = function(consent) {
        if (this.useLocalStorage && typeof localStorage !== 'undefined') {
            try {
                localStorage.setItem(this.cookieName, consent ? 'true' : 'false');
            } catch(e) {}
        } else if (typeof document !== 'undefined') {
            document.cookie = this.cookieName + '=' + (consent ? 'true' : 'false') + '; path=/; max-age=' + (60*60*24*365*10);
        }
    };
    CookiesEuBanner.prototype.hasConsent = function() {
        if (this.useLocalStorage && typeof localStorage !== 'undefined') {
            var stored = localStorage.getItem(this.cookieName);
            if (stored === 'true') return true;
            if (stored === 'false') return false;
            return null;
        } else if (typeof document !== 'undefined') {
            var match = document.cookie.match(new RegExp('(^|;)\\s*' + this.cookieName + '\\s*=\\s*([^;]+)'));
            if (match) {
                if (match[2] === 'true') return true;
                if (match[2] === 'false') return false;
            }
            return null;
        }
        return null;
    };
    CookiesEuBanner.prototype.deleteCookie = function(name) {
        if (this.useLocalStorage && typeof localStorage !== 'undefined') {
            try {
                localStorage.removeItem(name);
            } catch(e) {}
        } else if (typeof document !== 'undefined') {
            document.cookie = name + "=; Expires=Thu, 01 Jan 1970 00:00:01 GMT; Path=/;";
        }
    };
    CookiesEuBanner.prototype.addClickListener = function(el, fn) {
        if (el.addEventListener) {
            el.addEventListener('click', fn, false);
        } else if (el.attachEvent) {
            el.attachEvent('onclick', fn);
        }
    };
    CookiesEuBanner.prototype.removeBanner = function() {
        if (typeof document === 'undefined') return;
        var banner = document.getElementById(this.bannerId);
        if (banner) {
            banner.style.display = 'none';
        }
    };
    CookiesEuBanner.prototype.showBanner = function() {
        if (typeof document === 'undefined') return;
        var banner = document.getElementById(this.bannerId);
        if (!banner) return;
        banner.style.display = 'block';

        var accept = banner.querySelector('.' + this.acceptBtnClass);
        if (accept) {
            this.addClickListener(accept, () => {
                this.setConsent(true);
                banner.style.display = 'none';
                this.launchFunction();
            });
        }
        var reject = banner.querySelector('.' + this.rejectBtnClass);
        if (reject) {
            this.addClickListener(reject, () => {
                this.setConsent(false);
                banner.style.display = 'none';
            });
        }
        var more = banner.querySelector('.' + this.moreBtnClass);
        if (more) {
            this.addClickListener(more, () => {
                this.deleteCookie(this.cookieName);
                if (typeof localStorage !== 'undefined') {
                    try {
                        localStorage.removeItem(this.cookieName);
                    } catch(e) {}
                }
                banner.style.display = 'none';
            });
        }
    };

    return CookiesEuBanner;
}));