const { expect } = require('chai');

describe('fed135_Kalm/index.js toplevel - public', () => {
  it('should have the same module exports (public test)', () => {
    // Intentionally reordering but testing same deep equality with different variable names
    const mainExport = require('../..');
    const realExport = require('../../src');
    expect(realExport).to.deep.equal(mainExport);
  });
});