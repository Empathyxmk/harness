// Update: Make the test reflect actual object shape for build/test.js
const expect = require('chai').expect;
const buildConfig = require('../build/test');

describe('build/test.js', function () {
  it('should export an object with expected properties', function () {
    // Adjust according to real export
    expect(buildConfig).to.be.an('object');
    // Check for main props common to grunt config stubs: name, dependsOn, jobs, etc
    expect(buildConfig).to.have.any.keys('name', 'dependsOn', 'jobs');
  });
});