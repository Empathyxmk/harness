const { expect } = require('chai');
const util = require('../lib/util');

// Use different data for public test
describe('util (public)', function () {
  it('should have getJobs and getOptions as functions', function () {
    expect(util).to.have.property('getJobs').that.is.a('function');
    expect(util).to.have.property('getOptions').that.is.a('function');
  });

  it('getJobs should return array of jobs for different config', function () {
    // Pass dummy data; expect array result (structure, not contents)
    const jobs = util.getJobs({ testKey: 'public-value' });
    expect(jobs).to.be.an('array');
  });

  it('getOptions should process a different options object', function () {
    const opts = util.getOptions({ foo: 'bar', baz: 123 });
    expect(opts).to.be.an('object');
  });
});