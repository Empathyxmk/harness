// Public test for examples/dynamicKeys.js using different mock table/data flows
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/dynamicKeys.js (public)', () => {
  let log, originalExit;
  beforeEach(() => {
    log = [];
    originalExit = process.exit;
    process.exit = sinon.spy();
    console.log = (...args) => log.push(args.join(' '));
  });
  afterEach(() => {
    process.exit = originalExit;
  });

  it('should exit on createTables failure (public)', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: sinon.stub().returns({
        create: sinon.spy(),
        scan: () => ({ loadAll: () => ({ exec: sinon.spy() }) })
      }),
      createTables: (tables, cb) => cb(new Error('sim fail!'))
    };
    proxyquire('../examples/dynamicKeys', {
      '../index': fakeDynogels,
      joi: {},
      async: { times: (n, fn, cb) => cb() },
      lodash: {},
      util: { inspect: () => '{}'}
    });
    setImmediate(() => {
      sinon.assert.calledOnce(process.exit);
      done();
    });
  });

  it('should create DynamicModel items with different fields (public, happy)', (done) => {
    const created = [];
    function create(data, cb) {
      created.push(data);
      cb(null, data);
    }
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: sinon.stub().returns({
        create,
        scan: () => ({
          loadAll: () => ({
            exec: (cb) => cb(null, {
              Count: 3,
              Items: [
                { attrs: { id: 'X', foo: 7 } },
                { attrs: { id: 'Z', bar: 8 } },
                { attrs: { id: 'Y', baz: 9 } }
              ]
            })
          })
        })
      }),
      createTables: (tables, cb) => cb(null)
    };
    const fakeAsync = {
      times: (n, fn, cb) => {
        // three unique test ids
        fn(0, () => create({ id: 'X', foo: 7 }, () => {}));
        fn(1, () => create({ id: 'Z', bar: 8 }, () => {}));
        fn(2, () => create({ id: 'Y', baz: 9 }, () => {}));
        cb();
      }
    };
    proxyquire('../examples/dynamicKeys', {
      '../index': fakeDynogels,
      joi: {},
      async: fakeAsync,
      lodash: { pluck: arr => arr.map(i => i.attrs) },
      util: { inspect: obj => JSON.stringify(obj) }
    });

    setImmediate(() => {
      // Look for log with "Found 3 items"
      if (!log.some(l => l.includes('Found 3 items'))) throw new Error('Did not find items log');
      done();
    });
  });
});