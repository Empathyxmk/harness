const Emitter = require('../src/emitter');

describe('Emitter edge branch coverage - public data', function () {
    it('should handle off for another unknown event gracefully', function () {
        const e = new Emitter();
        expect(() => e.off('notARealEvent', () => {})).not.toThrow();
    });

    it('should call listeners for another event with multiple listeners', function () {
        const e = new Emitter();
        let cb1 = jest.fn(), cb2 = jest.fn();
        e.on('b', cb1);
        e.on('b', cb2);
        e.trigger('b', 10);
        expect(cb1).toHaveBeenCalledWith(10);
        expect(cb2).toHaveBeenCalledWith(10);
    });

    it('should only remove the intended handler with off for different handlers', function () {
        const e = new Emitter();
        let log = [];
        function handlerA() { log.push('A'); }
        function handlerB() { log.push('B'); }

        e.on('eventX', handlerA);
        e.on('eventX', handlerB);
        e.off('eventX', handlerB);
        e.trigger('eventX');
        expect(log).toEqual(['A']);
    });

    it('should not throw when triggering another event with no listeners', function () {
        const e = new Emitter();
        expect(() => e.trigger('noOneListening')).not.toThrow();
    });

    it('should remove all listeners for an event if no callback passed to off - public', function () {
        const e = new Emitter();
        let called = 0;
        function handler() { called += 1; }
        e.on('z', handler);
        e.off('z');
        e.trigger('z');
        expect(called).toBe(0);
    });

    it('should remove listeners even if removed multiple times for another event', function () {
        const e = new Emitter();
        let called = 0;
        function handler() { called += 1; }
        e.on('dup', handler);
        e.off('dup', handler);
        e.off('dup', handler);
        e.trigger('dup');
        expect(called).toBe(0);
    });

    it('should allow chaining of on and off with a new event', function () {
        const e = new Emitter();
        function cb() {}
        expect(e.on('yy', cb)).toBe(e);
        expect(e.off('yy', cb)).toBe(e);
    });
});