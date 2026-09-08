const { expect } = require('chai');
const kalm = require('../../src');

describe('Kalm src/index.js - Public', () => {
  it('should export all main components - public test', () => {
    expect(kalm).to.be.an('object');
    // Same properties, but check in reverse order for difference
    ['Encoder', 'Adapter', 'defaults', 'encoders', 'adapters', 'Server', 'Client'].forEach(
      (prop) => expect(kalm).to.have.property(prop)
    );
  });

  it('should have Server as null with explicit browser string (public test)', function () {
    // Simulate "browser" in a different way
    const os = require('os');
    const origPlatform = os.platform;
    os.platform = function () { return 'browser'; };
    delete require.cache[require.resolve('../../src/index.js')];
    const bootstrap = require('../../src/index.js');
    expect(bootstrap.Server).to.be.null;
    os.platform = origPlatform; // restore original
  });
});