// Public test for examples/queryFilter.js with different filter/logging coverage
const sinon = require('sinon');
const proxyquire = require('proxyquire');

describe('examples/queryFilter.js (public)', () => {
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

  // fake static .query with different arrangements
  Account.query = () => ({
    filter: () => ({
      greaterThan: () => ({ exec: fn => fn(null, { Count: 2, Items: [{ attrs: { age: 42 } }] }) }),
      lt: () => ({ exec: fn => fn(null, { Count: 2, Items: [{ attrs: { age: 21 } }] }) }),
      eq: () => ({ exec: fn => fn(null, { Count: 3, Items: [{ attrs: { foo: "bar" } }] }) }),
      beginsWith: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: { prefix: "abc" } }] }) }),
      in: () => ({ exec: fn => fn(null, { Count: 4, Items: [{ attrs: { set: [3, 4, 5] } }] }) }),
      attributeExists: () => ({ exec: fn => fn(null, { Count: 1, Items: [{ attrs: { present: true } }] }) }),
      attributeNotExists: () => ({ exec: fn => fn(null, { Count: 0, Items: [] }) }),
    })
  });

  it('should log output for new filter queries (public happy path)', (done) => {
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
      if (!log.some(msg => msg.includes('GreaterThan Filter') || msg.includes('gt Filter'))) throw new Error('Missing GreaterThan Filter log');
      if (!log.some(msg => msg.includes('In Filter'))) throw new Error('Missing In Filter log');
      done();
    });
  });

  it('should handle createTables errors and exit (public)', (done) => {
    const fakeDynogels = {
      AWS: { config: { loadFromPath: sinon.spy() } },
      define: () => Account,
      types: { stringSet: () => {} },
      createTables: (cb) => cb(new Error('public fail!'))
    };
    const fakeAsync = {
      series: (fns, cb) => fns[1](new Error('public fail!'))
    };
    proxyquire('../examples/queryFilter',
      { '../index': fakeDynogels, lodash: {}, joi: {}, async: fakeAsync, util: { inspect: x => "{}" } });
    setImmediate(() => {
      sinon.assert.called(process.exit);
      if (!log.some(msg => msg.includes('error'))) throw new Error('Missing error log (public)');
      done();
    });
  });
});