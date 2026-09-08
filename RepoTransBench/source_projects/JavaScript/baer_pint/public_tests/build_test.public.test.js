const { expect } = require('chai');
const fs = require('fs');
const path = require('path');

describe('build/test public', function () {
  // Use a different test file for public
  const buildTestDir = path.join(__dirname, '..', '.build_test_public');
  const testFile = path.join(buildTestDir, 'foo.test.js');
  before(() => {
    if (!fs.existsSync(buildTestDir)) fs.mkdirSync(buildTestDir);
    fs.writeFileSync(testFile, '// build public test');
  });
  after(() => {
    if (fs.existsSync(testFile)) fs.unlinkSync(testFile);
    if (fs.existsSync(buildTestDir)) fs.rmdirSync(buildTestDir);
  });

  it('should create a public build test file', function () {
    expect(fs.existsSync(testFile)).to.be.true;
    const content = fs.readFileSync(testFile, 'utf8');
    expect(content).to.contain('public');
  });

  it('should clean up public build test directory', function () {
    // Remove file and make sure it goes away
    fs.unlinkSync(testFile);
    expect(fs.existsSync(testFile)).to.be.false;
    // Restore for after hook
    fs.writeFileSync(testFile, '// build public test');
  });
});