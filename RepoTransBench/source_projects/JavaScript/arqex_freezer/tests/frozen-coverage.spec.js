const { expect } = require('chai');
const createFrozen = require('../src/frozen');
const utils = require('../src/utils');

describe('frozen.js basics', () => {
    it('should freeze arrays', () => {
        let frozen = createFrozen([1,2,3]);
        expect(utils.isArray(frozen)).to.be.true;
        expect(frozen[0]).to.equal(1);
    });

    it('should freeze objects', () => {
        let obj = {a:1, b:{c:2}};
        let frozen = createFrozen(obj);
        expect(frozen.a).to.equal(1);
    });

    it('should return the same primitive', () => {
        let x = 42;
        expect(createFrozen(x)).to.equal(42);
    });

    it('should throw on cyclic structures', () => {
        let obj = {};
        obj.self = obj;
        expect(() => createFrozen(obj)).to.throw();
    });
});