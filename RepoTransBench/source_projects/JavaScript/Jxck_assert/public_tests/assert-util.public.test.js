// Public tests for assert.js API: fresh values but parallel coverage to internal tests

const assert = require('../assert');

describe('assert basic API (public values)', () => {
    it('assert.ok truthy', () => {
        expect(() => assert.ok('nonempty')).not.toThrow();
        expect(() => assert.ok(42)).not.toThrow();
    });

    it('assert.ok falsy throws', () => {
        expect(() => assert.ok(null)).toThrow();
        expect(() => assert.ok(undefined)).toThrow();
    });

    it('assert.equal', () => {
        expect(() => assert.equal('abc', 'abc')).not.toThrow();
        expect(() => assert.equal('5', 5)).not.toThrow();
        expect(() => assert.equal('foo', 'bar')).toThrow();
    });

    it('assert.notEqual', () => {
        expect(() => assert.notEqual('dog', 'cat')).not.toThrow();
        expect(() => assert.notEqual('abc', 'abc')).toThrow();
    });

    it('assert.deepEqual', () => {
        expect(() => assert.deepEqual({m:{n:9}}, {m:{n:9}})).not.toThrow();
        expect(() => assert.deepEqual({a:2}, {a:3})).toThrow();
    });

    it('assert.notDeepEqual', () => {
        expect(() => assert.notDeepEqual({p:1}, {p:2})).not.toThrow();
        expect(() => assert.notDeepEqual({p:2}, {p:2})).toThrow();
    });

    it('assert.strictEqual and notStrictEqual', () => {
        expect(() => assert.strictEqual('hi', 'hi')).not.toThrow();
        expect(() => assert.strictEqual(2, '2')).toThrow();
        expect(() => assert.notStrictEqual(11, 22)).not.toThrow();
        expect(() => assert.notStrictEqual(22, 22)).toThrow();
    });

    it('assert.throws', () => {
        expect(() => assert.throws(() => { throw new TypeError("err") })).not.toThrow();
        expect(() => assert.throws(() => {})).toThrow();
    });

    it('assert.doesNotThrow', () => {
        expect(() => assert.doesNotThrow(() => { let a = 1+1; })).not.toThrow();
        expect(() => assert.doesNotThrow(() => { throw new Error("fail"); })).toThrow();
    });

    it('assert.ifError', () => {
        expect(() => assert.ifError(false)).not.toThrow();
        expect(() => assert.ifError(0)).not.toThrow();
        expect(() => assert.ifError('')).not.toThrow();
        expect(() => assert.ifError(new Error('kaboom'))).toThrow();
    });
});

describe('assert error message customization and edge branches (public)', () => {
    it('assert.ok with custom message', () => {
        try {
            assert.ok(null, "should be truthy!");
        } catch (e) {
            expect(e.message).toBe("should be truthy!");
        }
    });
    it('assert.equal with message', () => {
        try {
            assert.equal('abc', 'def', "not the same");
        } catch (e) {
            expect(e.message).toBe("not the same");
        }
    });
    it('assert.deepEqual with objects', () => {
        expect(() => assert.deepEqual({bar: 99}, {bar: 99})).not.toThrow();
        expect(() => assert.deepEqual({bar: 101}, {bar: 202})).toThrow();
    });
    it('assert.notDeepEqual with different objects', () => {
        expect(() => assert.notDeepEqual({z: 10}, {z: 20})).not.toThrow();
        expect(() => assert.notDeepEqual({z: 88}, {z: 88})).toThrow();
    });
});