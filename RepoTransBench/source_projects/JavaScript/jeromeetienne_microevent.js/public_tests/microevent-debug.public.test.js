const MicroEvent = require('../microevent-debug.js');

describe('MicroEvent-debug core (public)', () => {
    function createObj() {
        function Y() {}
        MicroEvent.mixin(Y);
        return new Y();
    }

    test('bind & trigger (debug, values changed)', () => {
        const obj = createObj();
        const fn = jest.fn();
        obj.bind('somethingNew', fn);
        obj.trigger('somethingNew', 88, 'zeta');
        expect(fn).toHaveBeenCalledWith(88, 'zeta');
    });

    test('unbind missing handler triggers assert (debug, public)', () => {
        const obj = createObj();
        const handler = () => {};

        // Actually bind a handler, then unbind a different one (public)
        obj.bind('pubEvent', handler);

        // Expect assert to be called
        const bogusHandler = () => {};
        const spy = jest.spyOn(console, 'assert').mockImplementation(() => {});

        obj.unbind('pubEvent', bogusHandler);

        expect(console.assert).toHaveBeenCalled();
        spy.mockRestore();
    });

    test('unbind real handler removes it (debug, public)', () => {
        const obj = createObj();
        const handler = jest.fn();
        obj.bind('alpha', handler);
        const s = jest.spyOn(console, 'assert').mockImplementation(() => {});
        obj.unbind('alpha', handler);
        obj.trigger('alpha', 42, 'omega');
        expect(handler).not.toHaveBeenCalled();
        s.mockRestore();
    });

    test('trigger on novel event is a no-op (debug, public)', () => {
        const obj = createObj();
        expect(() => obj.trigger('somethingNewer')).not.toThrow();
    });

    test('mixin returns undefined for debug (public)', () => {
        const obj = {};
        expect(MicroEvent.mixin(obj)).toBeUndefined(); // debug version returns undefined still
    });
});