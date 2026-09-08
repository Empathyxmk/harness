const Emitter = require('../src/emitter');

describe('Emitter edge branch coverage', function () {
    it('should handle off for unknown events gracefully', function () {
        const e = new Emitter();
        expect(() => e.off('notRegistered', () => {})).not.toThrow();
    });

    it('should call listeners for multiple events', function () {
        const e = new Emitter();
        let cb1 = jest.fn(), cb2 = jest.fn();
        e.on('a', cb1);
        e.on('a', cb2);
        e.trigger('a', 5);
        expect(cb1).toHaveBeenCalledWith(5);
        expect(cb2).toHaveBeenCalledWith(5);
    });

    it('should only remove the intended handler with off', function () {
        const e = new Emitter();
        let log = [];
        function handler1() { log.push('h1'); }
        function handler2() { log.push('h2'); }

        e.on('evt', handler1);
        e.on('evt', handler2);
        e.off('evt', handler1);
        e.trigger('evt');
        expect(log).toEqual(['h2']);
    });

    it('should not throw when triggering an event with no listeners', function () {
        const e = new Emitter();
        expect(() => e.trigger('noListeners')).not.toThrow();
    });

    it('should remove all listeners for an event if no callback passed to off', function () {
        const e = new Emitter();
        let called = 0;
        function handler() { called += 1; }
        e.on('e', handler);
        e.off('e');
        e.trigger('e');
        expect(called).toBe(0);
    });

    it('should remove listeners even if removed multiple times', function () {
        const e = new Emitter();
        let called = 0;
        function handler() { called += 1; }
        e.on('rem', handler);
        e.off('rem', handler);
        e.off('rem', handler);
        e.trigger('rem');
        expect(called).toBe(0);
    });

    it('should allow chaining of on and off', function () {
        const e = new Emitter();
        function cb() {}
        expect(e.on('x', cb)).toBe(e);
        expect(e.off('x', cb)).toBe(e);
    });
});