const { expect } = require('chai');
const path = require('path');

describe('Gruntfile.js', () => {
  it('should export a function', () => {
    const gruntfile = require(path.resolve(__dirname, '../Gruntfile.js'));
    expect(gruntfile).to.be.a('function');
  });

  it('should not throw when Gruntfile function is called with mock grunt', () => {
    const gruntfile = require(path.resolve(__dirname, '../Gruntfile.js'));
    const mockGrunt = {
      initConfig: () => {},
      loadNpmTasks: () => {},
      registerTask: () => {}
    };
    expect(() => gruntfile(mockGrunt)).to.not.throw();
  });
});