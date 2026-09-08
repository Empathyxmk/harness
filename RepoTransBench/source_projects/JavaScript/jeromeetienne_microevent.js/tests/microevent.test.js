const MicroEvent = require('../microevent.js');

// Helper to create fresh event targets
function createObj() {
    function X() {}
    MicroEvent.mixin(X);
    return new X();
}

describe('MicroEvent core', () => {
    test('bind & trigger basic functionality', () => {
        const obj = createObj();
        const mockFn = jest.fn();

        obj.bind('test', mockFn);
        obj.trigger('test', 42, 'foo');
        expect(mockFn).toHaveBeenCalledWith(42, 'foo');
    });

    test('multiple events, only fire matching', () => {
        const obj = createObj();
        const handlerA = jest.fn();
        const handlerB = jest.fn();

        obj.bind('a', handlerA);
        obj.bind('b', handlerB);

        obj.trigger('b', 123);
        expect(handlerA).not.toHaveBeenCalled();
        expect(handlerB).toHaveBeenCalledWith(123);
    });

    test('unbind removes previously bound handler', () => {
        const obj = createObj();
        const handler = jest.fn();

        obj.bind('something', handler);
        obj.unbind('something', handler);
        obj.trigger('something', 'should not be called');
        expect(handler).not.toHaveBeenCalled();
    });

    test('unbind on unregistered event does nothing', () => {
        const obj = createObj();
        // should not throw
        expect(() => obj.unbind('does-not-exist', () => {})).not.toThrow();
    });

    test('trigger on non-existing event is a no-op', () => {
        const obj = createObj();
        expect(() => obj.trigger('never-bound')).not.toThrow();
    });

    test('mixin with object, not class', () => {
        const obj = {};
        MicroEvent.mixin(obj);
        let called = false;
        obj.bind && obj.bind('ok', () => called = true);
        obj.trigger && obj.trigger('ok');
        expect(called).toBe(true);
    });

    test('mixin returns destObject', () => {
        const obj = {};
        const result = MicroEvent.mixin(obj);
        expect(result).toBe(obj);
    });
});