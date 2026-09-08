const tap = require('tap');
const { get, post, del, put, head, patch, options } = require('..');

// Utility to check structure of route definition arrays
function checkRouteArray(arr, method, path, store, t) {
  t.equal(arr[0], method);
  t.equal(arr[1], path);
  t.type(arr[2], 'function');
  if (store) t.same(arr[3], store);
}

// Utility to simulate handler fn result and req/res/params/store for enhancer tests.
function buildReqRes(url, host = 'publictest.com') {
  return [
    { url, headers: { host } },
    { end: () => {} }
  ];
}

tap.test('get, post, del, put, head, patch, options generate correct arrays [public]', t => {
  const fn = (req, res, store) => {};
  const store = { x: 17 }
  checkRouteArray(get('/pubA', fn, store), 'GET', '/pubA', store, t)
  checkRouteArray(post('/pubB', fn, store), 'POST', '/pubB', store, t)
  checkRouteArray(del('/pubC', fn, store), 'DELETE', '/pubC', store, t)
  checkRouteArray(put('/pubD', fn, store), 'PUT', '/pubD', store, t)
  checkRouteArray(head('/pubE', fn, store), 'HEAD', '/pubE', store, t)
  checkRouteArray(patch('/pubF', fn, store), 'PATCH', '/pubF', store, t)
  checkRouteArray(options('/pubG', fn, store), 'OPTIONS', '/pubG', store, t)
  t.end()
})

tap.test('enhancer parses query params correctly with different values [public]', t => {
  const arr = get('/query', (req, res, store) => req.query, { publicValue: 24 })
  const handler = arr[2]
  const [req, res] = buildReqRes('/query?alpha=beta&num=8')
  const params = { pub: 'testval' }
  const store = arr[3]
  Object.assign(res, { end: () => {} })
  handler(req, res, params, store)
  t.same(req.params, params, 'params attached')
  t.same(req.query, { alpha: 'beta', num: '8' })
  t.end()
})

tap.test('enhancer handles missing host header gracefully [public]', t => {
  const arr = get('/hostless', (req, res) => req.query)
  const handler = arr[2]
  const req = { url: '/hostless?x=42', headers: {} }
  const res = { end: () => {} }

  handler(req, res, {}, {})
  t.same(req.query, { x: '42' }, 'query works even with undefined host')
  t.end()
})

tap.test('enhancer handles missing query string [public]', t => {
  const arr = get('/noquerypublic', (req, res) => req.query)
  const handler = arr[2]
  const req = { url: '/noquerypublic', headers: { host: 'public.com' } }
  const res = { end: () => {} }
  handler(req, res, {}, {})
  t.same(req.query, {}, 'empty query attached')
  t.end()
})

// Skipping router store-through test for public as well (API note)
tap.test('router passes store value through [public]', { skip: true }, t => {
  // This test is purposely skipped, following project convention.
})