'use strict';

const sinon = require('sinon');
const expect = require('chai').expect;

// For now just testing initial util structure if it exports defined properties
describe('util', function () {
  it('should load util and have expected methods', function () {
    const util = require('../lib/util');
    expect(util).to.be.an('object');
    expect(util).to.have.property('getJobs');
    expect(util).to.have.property('getPathRelativeToTarget');
  });
});