// Smoke/coverage test for examples/dynamicKeys.js's main flows and logging
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/dynamicKeys.js', () => {
  let logOut = [];
  let origExit;
  beforeEach(() => {
    logOut = [];
    origExit = process.exit;
    process.exit = sinon.spy();
    console.log = (...args) => logOut.push(args.join(' '));
  });
  afterEach(() => {
    process.exit = origExit;
  });

  it('should log error and exit on createTables error', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => ({
        create: sinon.spy()
      }),
      createTables: (tables, cb) => cb(new Error('🌋 fail'))
    };
    proxyquire('../examples/dynamicKeys', { '../index': fakeDynogels, joi: {}, async: {}, lodash: {} });
    setImmediate(() => {
      sinon.assert.called(process.exit);
      sinon.assert.match(logOut.join(' '), /Error creating tables/);
      done();
    });
  });

  it('should create items and scan, logging output (success path)', (done) => {
    let created = [];
    const DynamicModel = {
      create: (data, next) => { created.push(data); next(null, data); },
      scan: () => ({
        loadAll: function() { return this; },
        exec: function(cb) {
          cb(null, {
            Count: created.length,
            Items: created.map(x => ({ attrs: x }))
          });
        }
      })
    };
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => DynamicModel,
      createTables: (tables, cb) => cb(null)
    };
    const fakeLodash = { pluck: (arr, key) => arr.map(x => x[key]) };
    const fakeAsync = {
      times: (n, iter, next) => {
        let pending = n;
        for (let i = 0; i < n; i++) {
          iter(i, () => --pending === 0 && next());
        }
      }
    };
    proxyquire('../examples/dynamicKeys',
      { '../index': fakeDynogels, joi: {}, async: fakeAsync, util: { inspect: x => JSON.stringify(x) }, lodash: fakeLodash });
    setImmediate(() => {
      // We expect "Found 25 items" to be in logs
      if (!logOut.some(msg => msg.includes('Found 25 items'))) throw new Error('Missing scan output');
      done();
    });
  });
});