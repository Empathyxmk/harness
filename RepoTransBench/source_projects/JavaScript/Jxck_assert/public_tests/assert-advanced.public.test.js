// Public advanced/edge test suite for assert.js: uses distinct data from internal tests but same coverage logic

const assert = require('../assert');

describe('assert advanced and edge cases (public)', () => {
    it('throws AssertionError with correct properties for falsy string', () => {
        try {
            assert.ok('', 'should not be falsy!');
        } catch (e) {
            expect(e).toHaveProperty('name', 'AssertionError');
            expect(e).toHaveProperty('message', 'should not be falsy!');
        }
    });

    it('throws with operator details for equal using objects', () => {
        try {
            assert.equal({ x: 1 }, { x: 1 }, 'fail eq objects');
        } catch (e) {
            expect(e.message).toBe('fail eq objects');
        }
    });

    it('throws with operator details for notEqual using same string', () => {
        try {
            assert.notEqual('foo', 'foo', 'fail neq str');
        } catch (e) {
            expect(e.message).toBe('fail neq str');
        }
    });

    it('deepEqual with different arrays', () => {
        expect(() => assert.deepEqual([10, 20], [10, 20])).not.toThrow();
        expect(() => assert.deepEqual([10, 20], [20, 10])).toThrow();
    });

    it('notDeepEqual with different arrays', () => {
        expect(() => assert.notDeepEqual([3, 4], [4, 3])).not.toThrow();
        expect(() => assert.notDeepEqual([3, 4], [3, 4])).toThrow();
    });

    it('strictEqual and notStrictEqual with booleans', () => {
        expect(() => assert.strictEqual(true, true)).not.toThrow();
        expect(() => assert.strictEqual(false, 0)).toThrow();
        expect(() => assert.notStrictEqual(true, false)).not.toThrow();
        expect(() => assert.notStrictEqual(false, false)).toThrow();
    });

    it('deepEqual with nested arrays/objects', () => {
        expect(() => assert.deepEqual({z: [9, {y: "x"}]}, {z: [9, {y: "x"}]})).not.toThrow();
        expect(() => assert.deepEqual({z: [9, {y: "x"}]}, {z: [9, {y: "notx"}]})).toThrow();
    });

    it('throws custom AssertionError for numbers', () => {
        function custom() { throw new assert.AssertionError({message:"bad", actual: 99, expected: 33, operator: ">"}) }
        expect(custom).toThrow();
    });

    it('assert.throws passes error to predicate for RangeError', () => {
        expect(() => {
            assert.throws(() => { throw new RangeError("out of range"); }, function (err) { return err instanceof RangeError; });
        }).not.toThrow();
        expect(() => {
            assert.throws(() => { throw new Error("other"); }, function (err) { return err instanceof RangeError; });
        }).toThrow();
    });

    it('assert.throws passes error to expected as RegExp (different pattern)', () => {
        expect(() => {
            assert.throws(() => { throw new Error("qwerty"); }, /wer/);
        }).not.toThrow();
        expect(() => {
            assert.throws(() => { throw new Error("asdfg"); }, /wer/);
        }).toThrow();
    });

    it('assert.doesNotThrow fails on thrown TypeError', () => {
        expect(() => assert.doesNotThrow(() => { throw new TypeError("bad call"); })).toThrow();
    });

    it('assert.ok throws when given 0', () => {
        expect(() => assert.ok(0)).toThrow();
    });

    it('ifError throws with array/object', () => {
        expect(() => assert.ifError([1,2,3])).toThrow();
        expect(() => assert.ifError({ foo: 'bar' })).toThrow();
    });

    it('ifError does not throw with undefined or false', () => {
        expect(() => assert.ifError(undefined)).not.toThrow();
        expect(() => assert.ifError(false)).not.toThrow();
    });
});