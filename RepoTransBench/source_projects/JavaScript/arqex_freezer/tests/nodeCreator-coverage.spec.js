const { expect } = require('chai');
const nodeCreator = require('../src/nodeCreator');
const utils = require('../src/utils');

describe('nodeCreator.js basics', () => {
    it('should create array node', () => {
        const arr = [1,2,3];
        let node = nodeCreator.create('array', arr);
        expect(utils.isArray(node)).to.be.true;
        expect(node[0]).to.equal(1);
    });

    it('should create object node', () => {
        const obj = {a:1};
        let node = nodeCreator.create('object', obj);
        expect(utils.isObject(node)).to.be.true;
        expect(node.a).to.equal(1);
    });

    it('should reject unknown type', () => {
        expect(() => nodeCreator.create('blorp', {})).to.throw();
    });

    it('should check isFrozen false for simple data', () => {
        expect(nodeCreator.isFrozen(42)).to.be.false;
        expect(nodeCreator.isFrozen({})).to.be.false;
    });
});