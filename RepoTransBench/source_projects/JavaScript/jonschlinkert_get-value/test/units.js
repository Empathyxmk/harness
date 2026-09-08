"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const strict_1 = __importDefault(require("node:assert/strict"));
exports.default = get => {
    describe('get value:', () => {
        it('should return non-object when given as the first argument', () => {
            strict_1.default.deepStrictEqual(get(null), null);
            strict_1.default.deepStrictEqual(get('foo'), 'foo');
            strict_1.default.deepStrictEqual(get(['a']), ['a']);
        });
        it('should get a value', () => {
            strict_1.default.deepStrictEqual(get({ a: 'a', b: { c: 'd' } }, 'a'), 'a');
            strict_1.default.deepStrictEqual(get({ a: 'a', b: { c: 'd' } }, 'b.c'), 'd');
            strict_1.default.deepStrictEqual(get({ foo: 'bar' }, 'foo.zed'), undefined);
        });
        it('should get a property that has dots in the key', () => {
            strict_1.default.deepStrictEqual(get({ 'a.b': 'c' }, 'a.b'), 'c');
        });
        it('should support using dot notation to get nested values', () => {
            const fixture = {
                a: { locals: { name: { first: 'Brian' } } },
                b: { locals: { name: { last: 'Woodward' } } },
                c: { locals: { paths: ['a.txt', 'b.js', 'c.hbs'] } }
            };
            strict_1.default.deepStrictEqual(get(fixture, 'a.locals.name'), { first: 'Brian' });
            strict_1.default.deepStrictEqual(get(fixture, 'b.locals.name'), { last: 'Woodward' });
            strict_1.default.strictEqual(get(fixture, 'b.locals.name.last'), 'Woodward');
            strict_1.default.strictEqual(get(fixture, 'c.locals.paths.0'), 'a.txt');
            strict_1.default.strictEqual(get(fixture, 'c.locals.paths.1'), 'b.js');
            strict_1.default.strictEqual(get(fixture, 'c.locals.paths.2'), 'c.hbs');
        });
        it('should support a custom separator on options.separator', () => {
            const fixture = { 'a.b': { c: { d: 'e' } } };
            strict_1.default.strictEqual(get(fixture, 'a.b/c/d', { separator: '/' }), 'e');
            strict_1.default.strictEqual(get(fixture, 'a\\.b.c.d', { separator: /\\?\./ }), 'e');
        });
        it('should support a custom split function', () => {
            const fixture = { 'a.b': { c: { d: 'e' } } };
            strict_1.default.strictEqual(get(fixture, 'a.b/c/d', { split: path => path.split('/') }), 'e');
            strict_1.default.strictEqual(get(fixture, 'a\\.b.c.d', { split: path => path.split(/\\?\./) }), 'e');
        });
        it('should support a custom join character', () => {
            const fixture = { 'a-b': { c: { d: 'e' } } };
            const options = { joinChar: '-' };
            strict_1.default.strictEqual(get(fixture, 'a.b.c.d', options), 'e');
        });
        it('should support a custom join function', () => {
            const fixture = { 'a-b': { c: { d: 'e' } } };
            const options = {
                split: path => path.split(/[-\/]/),
                join: segs => segs.join('-')
            };
            strict_1.default.strictEqual(get(fixture, 'a/b-c/d', options), 'e');
        });
        it('should support a default value as the last argument', () => {
            const fixture = { foo: { c: { d: 'e' } } };
            strict_1.default.equal(get(fixture, 'foo.bar.baz', 'quz'), 'quz');
            strict_1.default.equal(get(fixture, 'foo.bar.baz', true), true);
            strict_1.default.equal(get(fixture, 'foo.bar.baz', false), false);
            strict_1.default.equal(get(fixture, 'foo.bar.baz', null), null);
        });
        it('should support options.default', () => {
            const fixture = { foo: { c: { d: 'e' } } };
            strict_1.default.equal(get(fixture, 'foo.bar.baz', { default: 'qux' }), 'qux');
            strict_1.default.equal(get(fixture, 'foo.bar.baz', { default: true }), true);
            strict_1.default.equal(get(fixture, 'foo.bar.baz', { default: false }), false);
            strict_1.default.equal(get(fixture, 'foo.bar.baz', { default: null }), null);
            strict_1.default.deepStrictEqual(get(fixture, 'foo.bar.baz', { default: { one: 'two' } }), { one: 'two' });
        });
        it('should support a custom function for validating the object', () => {
            const isEnumerable = Object.prototype.propertyIsEnumerable;
            const options = {
                isValid(key, obj) {
                    return isEnumerable.call(obj, key);
                }
            };
            const fixture = { 'a.b': { c: { d: 'e' } } };
            strict_1.default.strictEqual(get(fixture, 'a.b.c.d', options), 'e');
        });
        it('should support nested keys with dots', () => {
            strict_1.default.strictEqual(get({ 'a.b.c': 'd' }, 'a.b.c'), 'd');
            strict_1.default.strictEqual(get({ 'a.b': { c: 'd' } }, 'a.b.c'), 'd');
            strict_1.default.strictEqual(get({ 'a.b': { c: { d: 'e' } } }, 'a.b.c.d'), 'e');
            strict_1.default.strictEqual(get({ a: { b: { c: 'd' } } }, 'a.b.c'), 'd');
            strict_1.default.strictEqual(get({ a: { 'b.c': 'd' } }, 'a.b.c'), 'd');
            strict_1.default.strictEqual(get({ 'a.b.c.d': 'e' }, 'a.b.c.d'), 'e');
            strict_1.default.strictEqual(get({ 'a.b.c.d': 'e' }, 'a.b.c'), undefined);
            strict_1.default.strictEqual(get({ 'a.b.c.d.e.f': 'g' }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b.c.d.e': { f: 'g' } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b.c.d': { e: { f: 'g' } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b.c': { d: { e: { f: 'g' } } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b': { c: { d: { e: { f: 'g' } } } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ a: { b: { c: { d: { e: { f: 'g' } } } } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.deepStrictEqual(get({ 'a.b.c.d.e': { f: 'g' } }, 'a.b.c.d.e'), { f: 'g' });
            strict_1.default.deepStrictEqual(get({ 'a.b.c.d': { 'e.f': 'g' } }, 'a.b.c.d.e'), undefined);
            strict_1.default.deepStrictEqual(get({ 'a.b.c': { 'd.e.f': 'g' } }, 'a.b.c'), { 'd.e.f': 'g' });
            strict_1.default.deepStrictEqual(get({ 'a.b': { 'c.d.e.f': 'g' } }, 'a.b'), { 'c.d.e.f': 'g' });
            strict_1.default.deepStrictEqual(get({ a: { 'b.c.d.e.f': 'g' } }, 'a'), { 'b.c.d.e.f': 'g' });
            strict_1.default.strictEqual(get({ 'a.b.c.d.e': { f: 'g' } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b.c.d': { 'e.f': 'g' } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b.c': { 'd.e.f': 'g' } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b': { 'c.d.e.f': 'g' } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ a: { 'b.c.d.e.f': 'g' } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b': { 'c.d': { 'e.f': 'g' } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ 'a.b': { c: { 'd.e.f': 'g' } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ a: { 'b.c.d.e': { f: 'g' } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ a: { 'b.c.d': { 'e.f': 'g' } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ a: { 'b.c': { 'd.e.f': 'g' } } }, 'a.b.c.d.e.f'), 'g');
            strict_1.default.strictEqual(get({ a: { b: { 'c.d.e.f': 'g' } } }, 'a.b.c.d.e.f'), 'g');
        });
        it('should support return default when options.isValid returns false', () => {
            const fixture = { foo: { bar: { baz: 'qux' }, 'a.b.c': 'xyx', yyy: 'zzz' } };
            const options = val => {
                return Object.assign({}, {
                    default: val,
                    isValid(key) {
                        return key !== 'bar' && key !== 'a.b.c';
                    }
                });
            };
            strict_1.default.equal(get(fixture, 'foo.bar.baz', options('fez')), 'fez');
            strict_1.default.equal(get(fixture, 'foo.bar.baz', options(true)), true);
            strict_1.default.equal(get(fixture, 'foo.bar.baz', options(false)), false);
            strict_1.default.equal(get(fixture, 'foo.bar.baz', options(null)), null);
            strict_1.default.equal(get(fixture, 'foo.a.b.c', options('fez')), 'fez');
            strict_1.default.equal(get(fixture, 'foo.a.b.c', options(true)), true);
            strict_1.default.equal(get(fixture, 'foo.a.b.c', options(false)), false);
            strict_1.default.equal(get(fixture, 'foo.a.b.c', options(null)), null);
            strict_1.default.equal(get(fixture, 'foo.yyy', options('fez')), 'zzz');
        });
        it('should get a value from an array', () => {
            const fixture = {
                a: { paths: ['a.txt', 'a.js', 'a.hbs'] },
                b: {
                    paths: {
                        '0': 'b.txt',
                        '1': 'b.js',
                        '2': 'b.hbs',
                        3: 'b3.hbs'
                    }
                }
            };
            strict_1.default.strictEqual(get(fixture, 'a.paths.0'), 'a.txt');
            strict_1.default.strictEqual(get(fixture, 'a.paths.1'), 'a.js');
            strict_1.default.strictEqual(get(fixture, 'a.paths.2'), 'a.hbs');
            strict_1.default.strictEqual(get(fixture, 'b.paths.0'), 'b.txt');
            strict_1.default.strictEqual(get(fixture, 'b.paths.1'), 'b.js');
            strict_1.default.strictEqual(get(fixture, 'b.paths.2'), 'b.hbs');
            strict_1.default.strictEqual(get(fixture, 'b.paths.3'), 'b3.hbs');
        });
        it('should get a value from an object in an array', () => {
            strict_1.default.strictEqual(get({ a: { b: [{ c: 'd' }] } }, 'a.b.0.c'), 'd');
            strict_1.default.strictEqual(get({ a: { b: [{ c: 'd' }, { e: 'f' }] } }, 'a.b.1.e'), 'f');
        });
        it('should return `undefined` if the path is not found', () => {
            const fixture = { a: { b: {} } };
            strict_1.default.strictEqual(get(fixture, 'a.b.c'), undefined);
            strict_1.default.strictEqual(get(fixture, 'a.b.c.d'), undefined);
        });
        it('should get the specified property', () => {
            strict_1.default.deepStrictEqual(get({ a: 'aaa', b: 'b' }, 'a'), 'aaa');
            strict_1.default.deepStrictEqual(get({ first: 'Jon', last: 'Schlinkert' }, 'first'), 'Jon');
            strict_1.default.deepStrictEqual(get({ locals: { a: 'a' }, options: { b: 'b' } }, 'locals'), { a: 'a' });
        });
        it('should support passing a property formatted as an array', () => {
            strict_1.default.deepStrictEqual(get({ a: 'aaa', b: 'b' }, ['a']), 'aaa');
            strict_1.default.deepStrictEqual(get({ a: { b: { c: 'd' } } }, ['a', 'b', 'c']), 'd');
            strict_1.default.deepStrictEqual(get({ first: 'Harry', last: 'Potter' }, ['first']), 'Harry');
            strict_1.default.deepStrictEqual(get({ locals: { a: 'a' }, options: { b: 'b' } }, ['locals']), { a: 'a' });
        });
        it('should support escaped dots', () => {
            strict_1.default.deepStrictEqual(get({ 'a.b': 'a', b: { c: 'd' } }, 'a\\.b'), 'a');
            strict_1.default.deepStrictEqual(get({ 'a.b': { b: { c: 'd' } } }, 'a\\.b.b.c'), 'd');
        });
        it('should get the value of a deeply nested property', () => {
            strict_1.default.strictEqual(get({ a: { b: 'c', c: { d: 'e', e: 'f', g: { h: 'i' } } } }, 'a.c.g.h'), 'i');
        });
        it('should return the entire object if no property is passed', () => {
            strict_1.default.deepStrictEqual(get({ a: 'a', b: { c: 'd' } }), { a: 'a', b: { c: 'd' } });
        });
    });
    /**
     * These tests are from the "dot-prop" library
     */
    describe('dot-prop tests:', () => {
        it('should pass dot-prop tests', () => {
            const f1 = { foo: { bar: 1 } };
            strict_1.default.deepStrictEqual(get(f1), f1);
            f1[''] = 'foo';
            strict_1.default.deepStrictEqual(get(f1, ''), 'foo');
            strict_1.default.deepStrictEqual(get(f1, 'foo'), f1.foo);
            strict_1.default.deepStrictEqual(get({ foo: 1 }, 'foo'), 1);
            strict_1.default.deepStrictEqual(get({ foo: null }, 'foo'), null);
            strict_1.default.deepStrictEqual(get({ foo: undefined }, 'foo'), undefined);
            strict_1.default.deepStrictEqual(get({ foo: { bar: true } }, 'foo.bar'), true);
            strict_1.default.deepStrictEqual(get({ foo: { bar: { baz: true } } }, 'foo.bar.baz'), true);
            strict_1.default.deepStrictEqual(get({ foo: { bar: { baz: null } } }, 'foo.bar.baz'), null);
            strict_1.default.deepStrictEqual(get({ '\\': true }, '\\'), true);
            strict_1.default.deepStrictEqual(get({ '\\foo': true }, '\\foo'), true);
            strict_1.default.deepStrictEqual(get({ 'bar\\': true }, 'bar\\'), true);
            strict_1.default.deepStrictEqual(get({ 'foo\\bar': true }, 'foo\\bar'), true);
            strict_1.default.deepStrictEqual(get({ '\\.foo': true }, '\\\\.foo'), true);
            strict_1.default.deepStrictEqual(get({ 'bar\\.': true }, 'bar\\\\.'), true);
            strict_1.default.deepStrictEqual(get({ 'foo\\.bar': true }, 'foo\\\\.bar'), true);
            strict_1.default.deepStrictEqual(get({ foo: 1 }, 'foo.bar'), undefined);
            function fn() { }
            fn.foo = { bar: 1 };
            strict_1.default.deepStrictEqual(get(fn), fn);
            strict_1.default.deepStrictEqual(get(fn, 'foo'), fn.foo);
            strict_1.default.deepStrictEqual(get(fn, 'foo.bar'), 1);
            const f3 = { foo: null };
            strict_1.default.deepStrictEqual(get(f3, 'foo.bar'), undefined);
            strict_1.default.deepStrictEqual(get(f3, 'foo.bar', 'some value'), 'some value');
            strict_1.default.deepStrictEqual(get({ 'foo.baz': { bar: true } }, 'foo\\.baz.bar'), true);
            strict_1.default.deepStrictEqual(get({ 'fo.ob.az': { bar: true } }, 'fo\\.ob\\.az.bar'), true);
            strict_1.default.deepStrictEqual(get(null, 'foo.bar', false), false);
            strict_1.default.deepStrictEqual(get('foo', 'foo.bar', false), false);
            strict_1.default.deepStrictEqual(get([], 'foo.bar', false), false);
            strict_1.default.deepStrictEqual(get(undefined, 'foo.bar', false), false);
        });
        it('should use a custom options.isValid function', () => {
            const isEnumerable = Object.prototype.propertyIsEnumerable;
            const options = {
                isValid: (key, obj) => isEnumerable.call(obj, key)
            };
            const target = {};
            Object.defineProperty(target, 'foo', {
                value: 'bar',
                enumerable: false
            });
            strict_1.default.deepStrictEqual(get(target, 'foo', options), undefined);
            strict_1.default.deepStrictEqual(get({}, 'hasOwnProperty', options), undefined);
        });
        it('should return a default value', () => {
            strict_1.default.deepStrictEqual(get({ foo: { bar: 'a' } }, 'foo.fake'), undefined);
            strict_1.default.deepStrictEqual(get({ foo: { bar: 'a' } }, 'foo.fake.fake2'), undefined);
            strict_1.default.deepStrictEqual(get({ foo: { bar: 'a' } }, 'foo.fake.fake2', 'some value'), 'some value');
        });
        it('should pass all of the dot-prop tests', () => {
            const f1 = { foo: { bar: 1 } };
            strict_1.default.deepStrictEqual(get(f1), f1);
            strict_1.default.deepStrictEqual(get(f1, 'foo'), f1.foo);
            strict_1.default.deepStrictEqual(get({ foo: 1 }, 'foo'), 1);
            strict_1.default.deepStrictEqual(get({ foo: null }, 'foo'), null);
            strict_1.default.deepStrictEqual(get({ foo: undefined }, 'foo'), undefined);
            strict_1.default.deepStrictEqual(get({ foo: { bar: true } }, 'foo.bar'), true);
            strict_1.default.deepStrictEqual(get({ foo: { bar: { baz: true } } }, 'foo.bar.baz'), true);
            strict_1.default.deepStrictEqual(get({ foo: { bar: { baz: null } } }, 'foo.bar.baz'), null);
            strict_1.default.deepStrictEqual(get({ foo: { bar: 'a' } }, 'foo.fake.fake2'), undefined);
        });
    });
    /**
     * These tests are from the "object-path" library
     */
    describe('object-path .get tests', () => {
        function getTestObj() {
            return {
                a: 'b',
                b: {
                    c: [],
                    d: ['a', 'b'],
                    e: [{}, { f: 'g' }],
                    f: 'i'
                }
            };
        }
        it('should return the value using unicode key', () => {
            const obj = { '15\u00f8C': { '3\u0111': 1 } };
            strict_1.default.equal(get(obj, '15\u00f8C.3\u0111'), 1);
            strict_1.default.equal(get(obj, ['15\u00f8C', '3\u0111']), 1);
        });
        it('should return the value using dot in key (with array of segments)', () => {
            const obj = { 'a.b': { 'looks.like': 1 } };
            strict_1.default.equal(get(obj, ['a.b', 'looks.like']), 1);
        });
        // object-path fails this test
        it('should return the value using dot in key', () => {
            const obj = { 'a.b': { 'looks.like': 1 } };
            strict_1.default.equal(get(obj, 'a.b.looks.like'), 1);
        });
        it('should return the value under shallow object', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj, 'a'), 'b');
            strict_1.default.equal(get(obj, ['a']), 'b');
        });
        it('should work with number path', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj.b.d, 0), 'a');
            strict_1.default.equal(get(obj.b, 0), undefined);
        });
        it('should return the value under deep object', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj, 'b.f'), 'i');
            strict_1.default.equal(get(obj, ['b', 'f']), 'i');
        });
        it('should return the value under array', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj, 'b.d.0'), 'a');
            strict_1.default.equal(get(obj, ['b', 'd', 0]), 'a');
        });
        it('should return the value under array deep', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj, 'b.e.1.f'), 'g');
            strict_1.default.equal(get(obj, ['b', 'e', 1, 'f']), 'g');
        });
        it('should return undefined for missing values under object', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj, 'a.b'), undefined);
            strict_1.default.equal(get(obj, ['a', 'b']), undefined);
        });
        it('should return undefined for missing values under array', () => {
            const obj = getTestObj();
            strict_1.default.equal(get(obj, 'b.d.5'), undefined);
            strict_1.default.equal(get(obj, ['b', 'd', '5']), undefined);
        });
        it('should return the value under integer-like key', () => {
            const obj = { '1a': 'foo' };
            strict_1.default.equal(get(obj, '1a'), 'foo');
            strict_1.default.equal(get(obj, ['1a']), 'foo');
        });
        it('should return the default value when the key doesnt exist', () => {
            const obj = { '1a': 'foo' };
            strict_1.default.equal(get(obj, '1b', null), null);
            strict_1.default.equal(get(obj, ['1b'], null), null);
        });
        // this test differs from behavior in object-path. I was unable to figure
        // out exactly how the default values work in object-path.
        it('should return the default value when path is empty', () => {
            const obj = { '1a': 'foo' };
            strict_1.default.deepStrictEqual(get(obj, '', null), null);
            strict_1.default.deepStrictEqual(get(obj, []), undefined);
            strict_1.default.equal(get({}, ['1'], 'foo'), 'foo');
        });
        it('should return the default value when object is null or undefined', () => {
            strict_1.default.deepStrictEqual(get(null, 'test', 'a'), 'a');
            strict_1.default.deepStrictEqual(get(undefined, 'test', 'a'), 'a');
        });
        it('should not fail on an object with a null prototype', function assertSuccessForObjWithNullProto() {
            const foo = 'FOO';
            const objWithNullProto = Object.create(null);
            objWithNullProto.foo = foo;
            strict_1.default.equal(get(objWithNullProto, 'foo'), foo);
        });
        // this differs from object-path, which does not allow
        // the user to get non-own properties for some reason.
        it('should get non-"own" properties on function classes', () => {
            const Base = function () { };
            Base.prototype = {
                one: {
                    two: true
                }
            };
            const Extended = function () {
                Base.call(this, true);
            };
            Extended.prototype = Object.create(Base.prototype);
            const extended = new Extended();
            strict_1.default.equal(get(extended, 'one.two'), true);
            strict_1.default.equal(get(extended, ['one', 'two']), true);
            extended.enabled = true;
            strict_1.default.equal(get(extended, 'enabled'), true);
            strict_1.default.deepStrictEqual(get(extended, 'one'), { two: true });
        });
        // this differs from object-path, which does not allow
        // the user to get non-own properties for some reason.
        it('should get non-"own" properties on classes', () => {
            class Base {
                one = { two: true };
            }
            class Extended extends Base {
            }
            const extended = new Extended();
            strict_1.default.equal(get(extended, 'one.two'), true);
            strict_1.default.equal(get(extended, ['one', 'two']), true);
            extended.enabled = true;
            strict_1.default.equal(get(extended, 'enabled'), true);
            strict_1.default.deepStrictEqual(get(extended, 'one'), { two: true });
        });
    });
    describe('deep-property unit tests', () => {
        it('should handle invalid input', () => {
            const a = undefined;
            const b = {};
            strict_1.default.equal(get(a, 'sample'), undefined);
            strict_1.default.deepStrictEqual(get(b, undefined), {});
            strict_1.default.deepStrictEqual(get(b, ''), undefined);
            strict_1.default.deepStrictEqual(get(b, '...'), undefined);
        });
        it('should get shallow properties', () => {
            const fn = () => { };
            const a = {
                sample: 'string',
                example: fn,
                unknown: undefined
            };
            strict_1.default.equal(get(a, 'example'), fn);
            strict_1.default.equal(get(a, 'sample'), 'string');
            strict_1.default.equal(get(a, 'unknown'), undefined);
            strict_1.default.equal(get(a, 'invalid'), undefined);
        });
        it('should get deep properties', () => {
            const a = {
                b: { example: { type: 'vegetable' } },
                c: { example: { type: 'mineral' } }
            };
            strict_1.default.equal(get(a, 'b.example.type'), 'vegetable');
            strict_1.default.equal(get(a, 'c.example.type'), 'mineral');
            strict_1.default.equal(get(a, 'c.gorky.type'), undefined);
        });
        it('should get properties on non-objects', () => {
            const fn = () => { };
            // the commented out lines are from from the "deep-property" lib,
            // but it's invalid javascript. This is a good example of why it's always
            // better to use "use strict" (and lint your code).
            // const str = 'An example string';
            // const num = 42;
            fn.path = { to: { property: 'string' } };
            // str.path = { to: { property: 'string' } };
            // num.path = { to: { property: 'string' } };
            strict_1.default.equal(get(fn, 'path.to.property'), 'string');
            // assert.equal(get(str, 'path.to.property'), undefined);
            // assert.equal(get(num, 'path.to.property'), undefined);
        });
    });
};
