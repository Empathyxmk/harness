const MicroCache = require('../microcache.js');

describe('MicroCache', () => {
    let cache;
    beforeEach(() => {
        cache = new MicroCache();
    });

    test('should set and get values', () => {
        cache.set('a', 123);
        expect(cache.get('a')).toBe(123);
        expect(cache.contains('a')).toBe(true);
    });

    test('should return undefined if value not set', () => {
        expect(cache.get('b')).toBeUndefined();
        expect(cache.contains('b')).toBe(false);
    });

    test('should remove values', () => {
        cache.set('key', 'val');
        cache.remove('key');
        expect(cache.get('key')).toBeUndefined();
        expect(cache.contains('key')).toBe(false);
    });

    test('should return all values', () => {
        cache.set('x', 1);
        cache.set('y', 2);
        const values = cache.values();
        expect(values).toHaveProperty('x', 1);
        expect(values).toHaveProperty('y', 2);
    });

    test('getSet sets value if absent and returns it', () => {
        const v = cache.getSet('a', 100);
        expect(v).toBe(100);
        expect(cache.get('a')).toBe(100);
    });

    test('getSet does not overwrite present value', () => {
        cache.set('bar', 77);
        const v = cache.getSet('bar', 88);
        expect(v).toBe(77);
        expect(cache.get('bar')).toBe(77);
    });

    test('getSet sets using function if value not present', () => {
        let called = false;
        const v = cache.getSet('fn', () => { called = true; return 42; });
        expect(v).toBe(42);
        expect(called).toBe(true);
    });

    test('getSet does not call value function if key is present', () => {
        let called = false;
        cache.set('fn', 43);
        const v = cache.getSet('fn', () => { called = true; return 42; });
        expect(v).toBe(43);
        expect(called).toBe(false);
    });

    test('values returns internal state object', () => {
        cache.set('one', 1);
        cache.set('two', 2);
        const vals = cache.values();
        expect(typeof vals).toBe('object');
        expect(vals).toEqual({ one: 1, two: 2 });
    });
});