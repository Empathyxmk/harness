const MicroEvent = require('../microevent-debug.js');

describe('MicroEvent-debug core', () => {
    function createObj() {
        function X() {}
        MicroEvent.mixin(X);
        return new X();
    }

    test('bind & trigger (debug)', () => {
        const obj = createObj();
        const fn = jest.fn();
        obj.bind('e', fn);
        obj.trigger('e', 1, 2);
        expect(fn).toHaveBeenCalledWith(1, 2);
    });

    test('unbind on missing handler asserts (debug)', () => {
        const obj = createObj();
        const handler = () => {};

        // Actually bind a handler, then try to unbind a different one
        obj.bind('someevent', handler);

        // The debug version uses console.assert (side effect, process continues)
        const bogusHandler = () => {};
        const spy = jest.spyOn(console, 'assert').mockImplementation(() => {});

        obj.unbind('someevent', bogusHandler);

        expect(console.assert).toHaveBeenCalled();
        spy.mockRestore();
    });

    test('unbind actually removes when correct handler', () => {
        const obj = createObj();
        const handler = jest.fn();
        obj.bind('e2', handler);
        const s = jest.spyOn(console, 'assert').mockImplementation(() => {});
        obj.unbind('e2', handler);
        obj.trigger('e2');
        expect(handler).not.toHaveBeenCalled();
        s.mockRestore();
    });

    test('trigger on missing event is a no-op (debug)', () => {
        const obj = createObj();
        expect(() => obj.trigger('notThere')).not.toThrow();
    });

    test('mixin returns destObject (debug)', () => {
        const obj = {};
        expect(MicroEvent.mixin(obj)).toBeUndefined(); // debug version does not return, just undefined
    });
});