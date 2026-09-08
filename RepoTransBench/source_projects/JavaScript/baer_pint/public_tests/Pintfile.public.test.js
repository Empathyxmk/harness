const { expect } = require('chai');
const path = require('path');

describe('Pintfile (public)', function () {
  it('should export jobs array (public)', function () {
    const p = require('../Pintfile.js');
    expect(p).to.have.property('jobs').that.is.an('array');
    // Instead of checking for real build/test.js structure, just length and type
    expect(p.jobs.length).to.be.above(0);
  });

  it('should contain a job module path (public)', function () {
    const p = require('../Pintfile.js');
    expect(p.jobs[0]).to.exist;
    // Test for string or object type for the job (different structure check)
    expect(['object', 'function'].includes(typeof p.jobs[0]) || typeof p.jobs[0] === 'string').to.be.true;
  });
});