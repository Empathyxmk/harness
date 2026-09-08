const { expect } = require('chai');
const Emitter = require('../src/emitter');

describe('Emitter basics', () => {
    let emitter;
    beforeEach(() => emitter = new Emitter());

    it('should emit events to listeners', done => {
        emitter.on('event', data => {
            expect(data.x).to.equal(1);
            done();
        });
        emitter.emit('event', {x:1});
    });

    it('should remove listeners', () => {
        let called = 0;
        const fn = () => called++;
        emitter.on('boom', fn);
        emitter.off('boom', fn);
        emitter.emit('boom');
        expect(called).to.equal(0);
    });

    it('once() should fire only once', () => {
        let times = 0;
        emitter.once('o', () => times++);
        emitter.emit('o');
        emitter.emit('o');
        expect(times).to.equal(1);
    });
});