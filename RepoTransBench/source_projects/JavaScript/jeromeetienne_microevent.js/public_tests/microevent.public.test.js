const MicroEvent = require('../microevent.js');

// Helper to create fresh event targets
function createObj() {
    function Y() {}
    MicroEvent.mixin(Y);
    return new Y();
}

describe('MicroEvent core (public)', () => {
    test('bind & trigger with alternate values', () => {
        const obj = createObj();
        const mockFn = jest.fn();

        obj.bind('alt', mockFn);
        obj.trigger('alt', 99, 'bar');
        expect(mockFn).toHaveBeenCalledWith(99, 'bar');
    });

    test('multiple different events; only matching is fired', () => {
        const obj = createObj();
        const handlerX = jest.fn();
        const handlerY = jest.fn();

        obj.bind('x', handlerX);
        obj.bind('y', handlerY);

        obj.trigger('x', 321);
        expect(handlerY).not.toHaveBeenCalled();
        expect(handlerX).toHaveBeenCalledWith(321);
    });

    test('unbind removes a handler: public version', () => {
        const obj = createObj();
        const handler = jest.fn();

        obj.bind('another', handler);
        obj.unbind('another', handler);
        obj.trigger('another', 'still not called');
        expect(handler).not.toHaveBeenCalled();
    });

    test('unbind from never-bound event (alternate, public)', () => {
        const obj = createObj();
        // should not throw
        expect(() => obj.unbind('not-there', () => {})).not.toThrow();
    });

    test('trigger on never-bound event does nothing (public)', () => {
        const obj = createObj();
        expect(() => obj.trigger('notThereAgain')).not.toThrow();
    });

    test('mixin on object-literal works (public)', () => {
        const obj = {};
        MicroEvent.mixin(obj);
        let called = false;
        obj.bind && obj.bind('pub', () => called = true);
        obj.trigger && obj.trigger('pub');
        expect(called).toBe(true);
    });

    test('mixin returns destObject (public)', () => {
        const obj = {};
        const result = MicroEvent.mixin(obj);
        expect(result).toBe(obj);
    });
});