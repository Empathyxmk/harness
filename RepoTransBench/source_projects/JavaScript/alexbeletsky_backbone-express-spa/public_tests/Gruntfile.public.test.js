const { expect } = require('chai');
const path = require('path');

describe('Gruntfile.js (public)', () => {
  it('should export a function (public)', () => {
    // Use a different property check to ensure function arity (length)
    const gruntfile = require(path.resolve(__dirname, '../Gruntfile.js'));
    expect(gruntfile.length).to.be.at.least(1); // Function expecting at least one argument
  });

  it('should handle multiple calls with different mock grunt (public)', () => {
    const gruntfile = require(path.resolve(__dirname, '../Gruntfile.js'));
    // Different mock grunt with additional property
    const mockGrunt = {
      initConfig: () => {},
      loadNpmTasks: () => {},
      registerTask: () => {},
      myCustomMethod: () => {}
    };
    gruntfile(mockGrunt); // Should not throw
    // Call twice
    gruntfile(mockGrunt);
  });
});