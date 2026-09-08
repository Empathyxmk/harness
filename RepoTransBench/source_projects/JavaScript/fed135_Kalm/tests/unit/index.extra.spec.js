const { expect } = require('chai');
const kalm = require('../../src');

describe('Kalm src/index.js', () => {
  it('should export components', () => {
    expect(kalm).to.be.an('object');
    expect(kalm).to.have.property('Client');
    expect(kalm).to.have.property('Server');
    expect(kalm).to.have.property('adapters');
    expect(kalm).to.have.property('encoders');
    expect(kalm).to.have.property('defaults');
    expect(kalm).to.have.property('Adapter');
    expect(kalm).to.have.property('Encoder');
  });

  it('should have Server null in "browser" condition', function() {
    // Simulate os.platform() returns 'browser'
    const os = require('os');
    const platform = os.platform;
    os.platform = () => 'browser';
    delete require.cache[require.resolve('../../src/index.js')];
    const bootstrap = require('../../src/index.js');
    expect(bootstrap.Server).to.equal(null);
    os.platform = platform;  // restore
  });
});