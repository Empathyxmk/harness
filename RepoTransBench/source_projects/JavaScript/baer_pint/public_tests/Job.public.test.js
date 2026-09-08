const fs = require('fs');
const path = require('path');
const { expect } = require('chai');
const Job = require('../lib/Job');

// Use a unique directory/filename for public test
const caskDir = path.join(__dirname, '..', '.cask_public');
const caskFile = path.join(caskDir, 'public.js');

describe('Job (public)', function () {
  before(() => {
    if (!fs.existsSync(caskDir)) fs.mkdirSync(caskDir);
    fs.writeFileSync(caskFile, '// dummy public.js content');
  });
  after(() => {
    if (fs.existsSync(caskFile)) fs.unlinkSync(caskFile);
    if (fs.existsSync(caskDir)) fs.rmdirSync(caskDir);
  });

  it('should initialize with a name and set config (public)', function () {
    const job = new Job('publictest');
    expect(job).to.have.property('name', 'publictest');
    expect(job).to.have.property('config');
  });

  it('should run and invoke success appropriately (public)', function (done) {
    let succeeded = false;
    const job = new Job('publictest');
    job.run({
      success: () => {
        succeeded = true;
        expect(succeeded).to.be.true;
        done();
      }
    });
  });

  it('should handle missing success callback gracefully (public)', function () {
    const job = new Job('publictest');
    expect(() => job.run({})).to.not.throw();
  });
});