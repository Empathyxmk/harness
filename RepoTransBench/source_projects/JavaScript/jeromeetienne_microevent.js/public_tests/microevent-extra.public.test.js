// Alternative data/branch-exercising public tests

const MicroEvent = require('../microevent.js');

describe("MicroEvent additional public branches", () => {
    test('unbind handler not present (no throw) - public', () => {
        function Qux() {}
        MicroEvent.mixin(Qux);
        const q = new Qux();
        function handler1() {}
        q.bind('z', handler1);
        // Try to remove an unrelated function; should not throw
        expect(() => q.unbind('z', function diff() {})).not.toThrow();
        // original handler still works
        const cb2 = jest.fn();
        q.bind('z', cb2);
        q.trigger('z', 'hello');
        expect(cb2).toHaveBeenCalled();
    });

    test('mixin on function/class twice (public)', () => {
        function Baz() {}
        MicroEvent.mixin(Baz);
        // call mixin again
        expect(() => MicroEvent.mixin(Baz)).not.toThrow();
        const b = new Baz();
        const fn = jest.fn();
        b.bind('evt', fn);
        b.trigger('evt', 555, 'alpha');
        expect(fn).toHaveBeenCalledWith(555, 'alpha');
    });
});

const MicroEventDebug = require('../microevent-debug.js');
describe("MicroEvent-debug public uncovered", () => {
    test('unbind on never-bound event in debug, alternate key', () => {
        function D() {}
        MicroEventDebug.mixin(D);
        const obj = new D();
        const spy = jest.spyOn(console, 'assert').mockImplementation(() => {});
        obj.unbind('never-seen', function(){});
        expect(spy).not.toHaveBeenCalledWith(false);
        spy.mockRestore();
    });

    test('bind multiple handlers/unbind one, with far values', () => {
        function D() {}
        MicroEventDebug.mixin(D);
        const obj = new D();
        const handler1 = jest.fn();
        const handler2 = jest.fn();
        obj.bind('humpty', handler1);
        obj.bind('humpty', handler2);
        const spy = jest.spyOn(console, 'assert').mockImplementation(() => {});
        obj.unbind('humpty', handler1);
        spy.mockRestore();
        obj.trigger('humpty', 'egg');
        expect(handler2).toHaveBeenCalled();
        expect(handler1).not.toHaveBeenCalled();
    });
});