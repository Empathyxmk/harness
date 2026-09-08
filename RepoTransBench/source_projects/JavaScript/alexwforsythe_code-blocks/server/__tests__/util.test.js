const util = require('../util');

describe('cloneObj', () => {
    it('clones plain objects', () => {
        const a = { x: { y: [1,2] } };
        const b = util.cloneObj(a);
        expect(b).not.toBe(a);
        expect(b).toEqual(a);
        b.x.y.push(3);
        expect(a.x.y).not.toEqual(b.x.y);
    });
    it('returns argument if not object', () => {
        expect(util.cloneObj(null)).toBe(null);
        expect(util.cloneObj(1)).toBe(1);
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
            language: 'js', theme: 'light', noBackground: false
        })).toBe(false);
    });
});

describe('cacheSelection & alreadySelected', () => {
    it('cacheSelection always returns true, alreadySelected works', () => {
        expect(util.cacheSelection('test')).toBe(true);
        expect(util.alreadySelected('abc')).toBe(true);
        expect(util.alreadySelected('xyz')).toBe(false);
    });
});

describe('loadThemes', () => {
    it('returns array of "base-theme"', () => {
        expect(util.loadThemes({})).toEqual(['base-theme']);
    });
});

describe('getThemeCssFromCache', () => {
    it('returns null unless theme is "other"', () => {
        expect(util.getThemeCssFromCache({}, 'base-theme')).toBe(null);
        expect(util.getThemeCssFromCache({}, 'other')).toBe('css2');
    });
});