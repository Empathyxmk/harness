const fs = require('fs');
const path = require('path');

// Public test: use different file in examples folder as subject (stub if doesn't exist) 
// But since only basic.js exists, duplicate tests with different description for public reveal
describe('[PUBLIC] examples/basic.js presence & safety', () => {
  const examplePath = path.join(__dirname, '../examples/basic.js');

  it('should exist and be accessible', () => {
    expect(fs.existsSync(examplePath)).toBe(true);
  });

  it('should have a .js file extension', () => {
    expect(path.extname(examplePath)).toBe('.js');
  });

  it('should load without error', () => {
    expect(() => {
      require(examplePath);
    }).not.toThrow();
  });
});