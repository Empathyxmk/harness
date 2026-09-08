// Additional tests to exercise remaining uncovered branches/lines

const MicroEvent = require('../microevent.js');

describe("MicroEvent additional cases for uncovered branches", () => {
    test('unbind handler not in list (should not throw)', () => {
        function Foo() {}
        MicroEvent.mixin(Foo);
        const f = new Foo();
        function handler() {}
        f.bind('x', handler);
        // Try to remove a function that's not bound
        expect(() => f.unbind('x', function another() {})).not.toThrow();
        // original still works, so removing unbound has no effect
        const cb = jest.fn();
        f.bind('x', cb);
        f.trigger('x', 'ok');
        expect(cb).toHaveBeenCalled();
    });

    test('mixin on function/class multiple times does not error', () => {
        function Bar() {}
        MicroEvent.mixin(Bar);
        // Apply again to check idempotency
        expect(() => MicroEvent.mixin(Bar)).not.toThrow();
        const b = new Bar();
        const fn = jest.fn();
        b.bind('a', fn);
        b.trigger('a', 1);
        expect(fn).toHaveBeenCalledWith(1);
    });
});

const MicroEventDebug = require('../microevent-debug.js');
describe("MicroEvent-debug uncovered paths", () => {
    test('unbind on unbound event (should hit guard and assert)', () => {
        function F() {}
        MicroEventDebug.mixin(F);
        const obj = new F();
        const spy = jest.spyOn(console, 'assert').mockImplementation(() => {});
        obj.unbind('non-existing', function(){});
        expect(spy).not.toHaveBeenCalledWith(false);
        spy.mockRestore();
    });

    test('bind multiple handlers then unbind one (checks indexOf)', () => {
        function F() {}
        MicroEventDebug.mixin(F);
        const obj = new F();
        const handler1 = jest.fn();
        const handler2 = jest.fn();
        obj.bind('foo', handler1);
        obj.bind('foo', handler2);
        const spy = jest.spyOn(console, 'assert').mockImplementation(() => {});
        obj.unbind('foo', handler2);
        spy.mockRestore();
        obj.trigger('foo', 'value');
        expect(handler1).toHaveBeenCalled();
        expect(handler2).not.toHaveBeenCalled();
    });
});