'use strict';

const expect = require('chai').expect;

describe('Pintfile.js', function () {
  it('should export a jobs array', function () {
    const pf = require('../Pintfile.js');
    expect(pf).to.have.property('jobs');
    expect(pf.jobs).to.be.an('array');
  });
});