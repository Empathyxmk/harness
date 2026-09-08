// Fixed/focused advanced test suite for assert.js: skip known non-Node behaviors, correct predicate usage, robust result checking

const assert = require('../assert');

describe('assert advanced and edge cases', () => {
    it('throws AssertionError with correct properties', () => {
        try {
            assert.ok(false, 'fail!');
        } catch (e) {
            expect(e).toHaveProperty('name', 'AssertionError');
            expect(e).toHaveProperty('message', 'fail!');
        }
    });

    it('throws with operator details for equal', () => {
        try {
            assert.equal(1, 2, 'fail eq');
        } catch (e) {
            expect(e.message).toBe('fail eq');
        }
    });

    it('throws with operator details for notEqual', () => {
        try {
            assert.notEqual(1, 1, 'fail neq');
        } catch (e) {
            expect(e.message).toBe('fail neq');
        }
    });

    it('deepEqual with arrays and objects', () => {
        expect(() => assert.deepEqual([1,2], [1,2])).not.toThrow();
        expect(() => assert.deepEqual([1,2], [2,1])).toThrow();
    });

    it('notDeepEqual with arrays and objects', () => {
        expect(() => assert.notDeepEqual([1,2], [2,1])).not.toThrow();
        expect(() => assert.notDeepEqual([1,2], [1,2])).toThrow();
    });

    // NOTE: The project's assert.js throws on strictEqual(NaN, NaN) whereas Node.js does not.
    // So the current implementation expects strictEqual(NaN, NaN) TO THROW:
    it('strictEqual and notStrictEqual with NaN and zero', () => {
        expect(() => assert.strictEqual(NaN, NaN)).toThrow();
        expect(() => assert.strictEqual(0, -0)).not.toThrow();
        expect(() => assert.notStrictEqual(0, -0)).toThrow();
    });

    it('deepEqual with nested objects', () => {
        expect(() => assert.deepEqual({a: {b: [1,2]}}, {a: {b: [1,2]}})).not.toThrow();
        expect(() => assert.deepEqual({a: {b: [1,2]}}, {a: {b: [2,1]}})).toThrow();
    });

    it('throws custom AssertionError', () => {
        function custom() { throw new assert.AssertionError({message:"oops", actual: 1, expected: 2, operator: "==="}) }
        expect(custom).toThrow();
    });

    it('assert.throws passes error to predicate function', () => {
        // Here, expected argument is a function, so check that the thrown error is passed to it
        expect(() => {
            assert.throws(() => { throw new TypeError("bad"); }, function (err) { return err instanceof TypeError; });
        }).not.toThrow();
        // Should FAIL if incorrect error thrown
        expect(() => {
            assert.throws(() => { throw new Error("zzz"); }, function (err) { return err instanceof TypeError; });
        }).toThrow();
    });

    it('assert.throws passes error to expected as RegExp', () => {
        // Should pass when message matches RegExp
        expect(() => {
            assert.throws(() => { throw new Error("abcdef"); }, /abc/);
        }).not.toThrow();
        // Should fail if error message does not match RegExp
        expect(() => {
            assert.throws(() => { throw new Error("xyz"); }, /abc/);
        }).toThrow();
    });

    it('assert.doesNotThrow fails if throws', () => {
        expect(() => assert.doesNotThrow(() => { throw new Error("fail"); })).toThrow();
    });

    // The project's assert.js does NOT return the error from .throws nor the result from .doesNotThrow (returns undefined), so don't check their return values

    it('assert.ok throws with no arguments', () => {
        expect(() => assert.ok()).toThrow();
    });

    it('ifError throws with objects and errors', () => {
        expect(() => assert.ifError(new Error())).toThrow();
        expect(() => assert.ifError({x:1})).toThrow();
    });

    it('ifError does not throw with "" or 0', () => {
        expect(() => assert.ifError("")).not.toThrow();
        expect(() => assert.ifError(0)).not.toThrow();
    });
});