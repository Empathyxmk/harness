// Smoke test for examples/queryFilter.js for coverage of main happy/error paths + logging
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/queryFilter.js', () => {
  let log, origExit;
  beforeEach(() => {
    log = [];
    origExit = process.exit;
    process.exit = sinon.spy();
    console.log = (...args) => log.push(args.join(' '));
  });
  afterEach(() => {
    process.exit = origExit;
  });

  function Account() {}
  // fake static .query
  Account.query = () => ({
    filter: () => ({
      equals: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: {} }] }) }),
      between: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: {} }] }) }),
      in: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: {} }] }) }),
      exists: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: {} }] }) }),
      notContains: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: {} }] }) }),
      contains: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: {} }] }) })
    })
  });

  it('should eventually log output for main filter queries (happy path)', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => Account,
      types: { stringSet: () => {} },
      createTables: (cb) => cb(null)
    };
    const fakeLodash = { noop: () => {}, pluck: () => [] };
    const fakeAsync = {
      times: (n, fn, cb) => { for (let i = 0; i < n; i++) fn(i, () => {}); cb(); },
      series: (arr, cb) => arr[arr.length - 1](null, cb)
    };
    proxyquire('../examples/queryFilter',
      { '../index': fakeDynogels, lodash: fakeLodash, joi: {}, async: fakeAsync, util: { inspect: x => JSON.stringify(x) } });
    setImmediate(() => {
      // Should see logging for Filters
      if (!log.some(msg => msg.includes('Equals Filter'))) throw new Error('Missing Equals Filter log');
      if (!log.some(msg => msg.includes('Between Filter'))) throw new Error('Missing Between Filter log');
      done();
    });
  });

  it('should handle createTables errors and exit', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => Account,
      types: { stringSet: () => {} },
      createTables: (cb) => cb(new Error('fail!'))
    };
    const fakeAsync = {
      series: (fns, cb) => fns[1](new Error('fail!'))
    };
    proxyquire('../examples/queryFilter',
      { '../index': fakeDynogels, lodash: {}, joi: {}, async: fakeAsync, util: { inspect: x => "{}" } });
    setImmediate(() => {
      sinon.assert.called(process.exit);
      if (!log.some(msg => msg.includes('error'))) throw new Error('Missing error log');
      done();
    });
  });
});