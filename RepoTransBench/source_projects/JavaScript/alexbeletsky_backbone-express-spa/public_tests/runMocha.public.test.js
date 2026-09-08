const sinon = require('sinon');
const { expect } = require('chai');

describe('runMocha.js (public)', () => {
  it('should set environment vars and invoke scripts (public)', () => {
    const backupEnv = { ...process.env };
    process.env = { FOO: 'BAR' }; // different starting env
    const origRequire = global.require;
    global.require = (mod) => {}; // mock require

    const exitStub = sinon.stub(process, 'exit');

    require('../runMocha.js');

    // Test with uppercase
    expect(process.env.NODE_ENV.toUpperCase()).to.equal('DEVELOPMENT');
    expect(process.env.APP_ENV.toUpperCase()).to.equal('DEVELOPMENT');
    expect(process.env.TEST_ENV.toUpperCase()).to.equal('DEVELOPMENT');
    expect(process.env.CLIENTAPP_ENV.toUpperCase()).to.equal('DEVELOPMENT');

    exitStub.restore();
    global.require = origRequire;
    process.env = backupEnv;
  });
});