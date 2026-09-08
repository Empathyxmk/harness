// Public test for examples/optionalAttributes.js using different test data/branches
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/optionalAttributes.js (public)', () => {
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

  it('should exit when createTables fails with a different error (public)', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => {
        function Q() {}
        Q.create = sinon.spy();
        return Q;
      },
      createTables: (cb) => cb(new Error('different fail'))
    };
    proxyquire('../examples/optionalAttributes', { '../index': fakeDynogels, joi: {} });
    setImmediate(() => {
      sinon.assert.calledOnce(process.exit);
      done();
    });
  });

  it('should create and save two different Persons (with and without email) (public)', (done) => {
    function Person() {}
    Person.prototype.save = function (cb) { cb(null, { get: () => ({ email: 'foo@bar.com' }) }); };
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
      if (entries.length !== 2) throw new Error('Did not create/save persons (public)');
      done();
    });
  });
});