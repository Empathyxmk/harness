const MicroCache = require('../microcache.js');

describe('MicroCache (public test cases)', () => {
    let cache;
    beforeEach(() => {
        cache = new MicroCache();
    });

    test('should set and get values (public values)', () => {
        cache.set('cat', 789);
        expect(cache.get('cat')).toBe(789);
        expect(cache.contains('cat')).toBe(true);
    });

    test('should return undefined if value not set (public)', () => {
        expect(cache.get('dog')).toBeUndefined();
        expect(cache.contains('dog')).toBe(false);
    });

    test('should remove values (public)', () => {
        cache.set('publicKey', 'publicVal');
        cache.remove('publicKey');
        expect(cache.get('publicKey')).toBeUndefined();
        expect(cache.contains('publicKey')).toBe(false);
    });

    test('should return all values (public)', () => {
        cache.set('foo', 10);
        cache.set('bar', 20);
        const values = cache.values();
        expect(values).toHaveProperty('foo', 10);
        expect(values).toHaveProperty('bar', 20);
    });

    test('getSet sets value if absent and returns it (public)', () => {
        const v = cache.getSet('z', 200);
        expect(v).toBe(200);
        expect(cache.get('z')).toBe(200);
    });

    test('getSet does not overwrite present value (public)', () => {
        cache.set('baz', 101);
        const v = cache.getSet('baz', 303);
        expect(v).toBe(101);
        expect(cache.get('baz')).toBe(101);
    });

    test('getSet sets using function if value not present (public)', () => {
        let called = false;
        const v = cache.getSet('cb', () => { called = true; return 99; });
        expect(v).toBe(99);
        expect(called).toBe(true);
    });

    test('getSet does not call value function if key is present (public)', () => {
        let called = false;
        cache.set('cb', 55);
        const v = cache.getSet('cb', () => { called = true; return 99; });
        expect(v).toBe(55);
        expect(called).toBe(false);
    });

    test('values returns internal state object (public)', () => {
        cache.set('alpha', 1234);
        cache.set('beta', 5678);
        const vals = cache.values();
        expect(typeof vals).toBe('object');
        expect(vals).toEqual({ alpha: 1234, beta: 5678 });
    });
});