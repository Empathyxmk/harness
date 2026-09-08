const sinon = require('sinon');

describe('runMocha.js', () => {
  it('should set process.env vars and call underlying scripts', () => {
    const envBackup = { ...process.env };
    process.env = {};
    const _require = global.require;
    global.require = (mod) => {};

    const exitStub = sinon.stub(process, 'exit');

    require('../runMocha.js');

    expect(process.env.NODE_ENV).to.equal('development');
    expect(process.env.APP_ENV).to.equal('development');
    expect(process.env.TEST_ENV).to.equal('development');
    expect(process.env.CLIENTAPP_ENV).to.equal('development');
    
    exitStub.restore();
    global.require = _require;
    process.env = envBackup;
  });
});