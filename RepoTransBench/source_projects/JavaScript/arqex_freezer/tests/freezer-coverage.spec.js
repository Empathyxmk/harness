const { expect } = require('chai');
const Freezer = require('../src/freezer');

describe('Freezer core', () => {
    it('constructs and gets data', () => {
        const initial = {a: 1, b: 2};
        const store = new Freezer(initial);
        const data = store.get();
        expect(data.a).to.equal(1);
    });

    it('should update data and emit update event', done => {
        const store = new Freezer({ x: 1 });
        store.on('update', () => done());
        const d = store.get();
        d.x = 2;
        store.freeze({ x: 2 });
    });

    it('should support setOption', () => {
        const store = new Freezer({ n: 1 });
        store.setOption('mutable', true);
        expect(store.options.mutable).to.be.true;
    });

    it('should call reset', () => {
        const store = new Freezer({ n: 1 });
        store.reset({ n: 0 });
        expect(store.get().n).to.equal(0);
    });

    it('should call now', () => {
        const store = new Freezer({ m: 5 });
        expect(store.now()).to.be.a('number');
    });
});