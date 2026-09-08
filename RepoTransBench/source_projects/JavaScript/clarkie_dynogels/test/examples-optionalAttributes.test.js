// Smoke test for examples/optionalAttributes.js (covering happy and error paths)
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/optionalAttributes.js', () => {
  let log, originalExit;
  beforeEach(() => {
    log = [];
    originalExit = process.exit;
    process.exit = sinon.spy();
    console.log = (msg, ...rest) => log.push([msg, ...rest]);
  });
  afterEach(() => {
    process.exit = originalExit;
  });

  it('should handle failed createTables and exit', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => {
        function P() {}
        P.create = sinon.spy();
        return P;
      },
      createTables: (cb) => cb(new Error('fail'))
    };
    proxyquire('../examples/optionalAttributes', { '../index': fakeDynogels, joi: {} });
    setImmediate(() => {
      sinon.assert.calledOnce(process.exit);
      done();
    });
  });

  it('should create Person and save them (name not null and null)', (done) => {
    function Person() {}
    Person.prototype.save = function (cb) { cb(null, { get: () => ({ name: null }) }); };
    Person.create = function(data, cb) {
      cb(null, { get: () => data });
    };
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => Person,
      createTables: (cb) => cb(null)
    };
    proxyquire('../examples/optionalAttributes', { '../index': fakeDynogels, joi: {} });
    setImmediate(() => {
      // check for message "got person"
      const entries = log.filter(msg => Array.isArray(msg) && msg[0] === 'got person');
      if (entries.length !== 2) throw new Error('Did not create/save persons successfully');
      done();
    });
  });
});