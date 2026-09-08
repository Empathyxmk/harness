const { expect } = require('chai');

describe('fed135_Kalm/index.js toplevel', () => {
  it('should export the same as src', () => {
    const src = require('../..');
    const bootstrap = require('../../src');
    expect(src).to.deep.equal(bootstrap);
  });
});