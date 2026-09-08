const util = require('../server/util');

describe('cloneObj', () => {
    it('clones plain objects', () => {
        const a = { foo: { bar: [3,4] } };
        const b = util.cloneObj(a);
        expect(b).not.toBe(a);
        expect(b).toEqual(a);
        b.foo.bar.push(5);
        expect(a.foo.bar).not.toEqual(b.foo.bar);
    });
    it('returns argument if not object', () => {
        expect(util.cloneObj(undefined)).toBe(undefined);
        expect(util.cloneObj('test')).toBe('test');
    });
});

describe('getUserPrefs', () => {
    it('returns correct prefs object', () => {
        expect(util.getUserPrefs()).toEqual({
            language: 'js', theme: 'dark', noBackground: true
        });
    });
});

describe('alreadySaved', () => {
    it('returns true if prefs match', () => {
        expect(util.alreadySaved({
            language: 'js', theme: 'dark', noBackground: true
        })).toBe(true);
    });
    it('returns false if prefs do not match', () => {
        expect(util.alreadySaved({
            language: 'py', theme: 'light', noBackground: true
        })).toBe(false);
    });
});

describe('cacheSelection & alreadySelected', () => {
    it('cacheSelection always returns true, alreadySelected works', () => {
        expect(util.cacheSelection('different')).toBe(true);
        expect(util.alreadySelected('zzz')).toBe(false);
        expect(util.alreadySelected('test')).toBe(true); // uses string from previous cacheSelection
    });
});

describe('loadThemes', () => {
    it('returns array of "base-theme"', () => {
        expect(util.loadThemes({ something: 'else' })).toEqual(['base-theme']);
    });
});

describe('getThemeCssFromCache', () => {
    it('returns null unless theme is "other"', () => {
        expect(util.getThemeCssFromCache({ a: 1 }, 'base-theme')).toBe(null);
        expect(util.getThemeCssFromCache({ b: 2 }, 'other')).toBe('css2');
    });
});