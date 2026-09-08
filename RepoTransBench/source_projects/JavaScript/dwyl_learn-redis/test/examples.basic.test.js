const fs = require('fs');
const path = require('path');

// Test whether examples/basic.js exists and is a JavaScript file
describe('examples/basic.js', () => {
  const examplePath = path.join(__dirname, '../examples/basic.js');

  it('should exist', () => {
    expect(fs.existsSync(examplePath)).toBe(true);
  });

  it('should be a JavaScript file', () => {
    expect(examplePath.endsWith('.js')).toBe(true);
  });

  it('should not throw when loaded', () => {
    expect(() => {
      require(examplePath);
    }).not.toThrow();
  });
});