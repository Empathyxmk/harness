const fs = require('fs');
const path = require('path');
const { expect } = require('chai');
const Job = require('../lib/Job');

// Create the required directory for test to prevent ENOENT error
const caskDir = path.join(__dirname, '..', '.cask');
const caskFile = path.join(caskDir, 'test.js');

describe('Job', function () {
  before(() => {
    if (!fs.existsSync(caskDir)) fs.mkdirSync(caskDir);
    // Ensure the file exists with dummy content
    fs.writeFileSync(caskFile, '// dummy test.js content');
  });
  after(() => {
    if (fs.existsSync(caskFile)) fs.unlinkSync(caskFile);
    if (fs.existsSync(caskDir)) fs.rmdirSync(caskDir);
  });

  it('should initialize with a name and set config', function () {
    const job = new Job('test');
    expect(job).to.have.property('name', 'test');
    expect(job).to.have.property('config');
  });

  it('should run and invoke success appropriately', function (done) {
    let succeeded = false;
    const job = new Job('test');
    job.run({
      success: () => {
        succeeded = true;
        expect(succeeded).to.be.true;
        done();
      }
    });
  });

  it('should handle missing success callback gracefully', function () {
    const job = new Job('test');
    expect(() => job.run({})).to.not.throw();
  });
});