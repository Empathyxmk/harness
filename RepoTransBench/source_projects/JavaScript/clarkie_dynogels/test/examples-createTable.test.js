// Minimal functional test for examples/createTable.js to ensure error and success logging
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/createTable.js', () => {
  let log, originalExit, calledExit;

  beforeEach(() => {
    log = [];
    calledExit = false;
    // Patch process.exit so the script does not exit the test runner
    originalExit = process.exit;
    process.exit = () => { calledExit = true; };
  });

  afterEach(() => {
    process.exit = originalExit;
  });

  it('should log error when createTables callback gets error', (done) => {
    // Setup dynogels mock
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: sinon.stub(),
      createTables: (tables, callback) => callback(new Error('fail'))
    };
    // Patch console.log to capture logs for assertion
    const origConsole = console.log;
    console.log = (msg) => log.push(msg);

    proxyquire('../examples/createTable', { '../index': fakeDynogels, joi: {} });

    // Restore after import
    setImmediate(() => {
      console.log = origConsole;
      sinon.assert.match(log[log.length - 1], /Error creating tables/);
      done();
    });
  });

  it('should log success message when createTables callback succeeds', (done) => {
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
      sinon.assert.match(
        log.find(l => typeof l === 'string' && l.includes('created and active')),
        'table are now created and active'
      );
      done();
    });
  });
});