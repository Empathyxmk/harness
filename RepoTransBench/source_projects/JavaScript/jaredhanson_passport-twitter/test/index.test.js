const proxyquire = require('proxyquire').noCallThru();
const { expect } = require('chai');

describe('index.js', () => {
  it('should export Strategy and .Strategy', () => {
    const exp = require('../lib/index');
    expect(exp).to.equal(exp.Strategy);
  });
});