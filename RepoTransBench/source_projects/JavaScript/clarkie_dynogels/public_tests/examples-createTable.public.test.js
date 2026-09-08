// Public test for examples/createTable.js with different error/success branch coverage
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/createTable.js (public)', () => {
  let log, originalExit, calledExit;

  beforeEach(() => {
    log = [];
    calledExit = false;
    originalExit = process.exit;
    process.exit = () => { calledExit = true; };
  });

  afterEach(() => {
    process.exit = originalExit;
  });

  it('should log error for different error message (public)', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: sinon.stub(),
      createTables: (tables, callback) => callback(new Error('network unavailable'))
    };
    const origConsole = console.log;
    console.log = (msg) => log.push(msg);

    proxyquire('../examples/createTable', { '../index': fakeDynogels, joi: {} });

    setImmediate(() => {
      console.log = origConsole;
      sinon.assert.match(log.find(l => typeof l === 'string' && l.includes('Error creating tables')), /Error creating tables/);
      done();
    });
  });

  it('should log a different success message (public)', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: sinon.stub(),
      createTables: (tables, callback) => callback(null)
    };
    const origConsole = console.log;
    console.log = (msg) => log.push(msg);

    proxyquire('../examples/createTable', { '../index': fakeDynogels, joi: {} });

    setImmediate(() => {
      console.log = origConsole;
      // look for a different message, e.g., from a different object literal, if applicable
      sinon.assert.match(
        log.find(l => typeof l === 'string' && l.includes('created and active')),
        'table are now created and active'
      );
      done();
    });
  });
});