const Emitter = require('../src/emitter');

describe('Emitter coverage branches - public data', function() {
    it('should emit value to handler', function() {
        const e = new Emitter();
        let log = [];
        function handler(x) { log.push(x * 2); }
        e.on('event', handler);
        e.trigger('event', 21);
        expect(log).toEqual([42]);
    });

    it('should off handler and not call after off', function() {
        const e = new Emitter();
        let v = 0;
        function handler(n) { v = n; }
        e.on('test', handler);
        e.off('test', handler);
        e.trigger('test', 999);
        expect(v).toBe(0);
    });

    it('should support multiple events and handlers', function() {
        const e = new Emitter();
        let count = 0;
        e.on('x', () => count += 2);
        e.on('y', () => count += 3);
        e.trigger('x');
        e.trigger('y');
        expect(count).toBe(5);
    });

    it('trigger with multiple arguments', function() {
        const e = new Emitter();
        let args = [];
        function handler(a, b, c) { args = [a, b, c]; }
        e.on('multi', handler);
        e.trigger('multi', 'alpha', 'beta', 'gamma');
        expect(args).toEqual(['alpha', 'beta', 'gamma']);
    });

    it('off with no arguments removes all', function() {
        const e = new Emitter();
        let cnt = 0;
        function h1() { cnt += 11; }
        function h2() { cnt += 22; }
        e.on('E', h1);
        e.on('E', h2);
        e.off('E');
        e.trigger('E');
        expect(cnt).toBe(0);
    });
});