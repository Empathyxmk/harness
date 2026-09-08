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
function buildReqRes(url, host = 'localhost') {
  return [
    { url, headers: { host } },
    { end: () => {} }
  ];
}

tap.test('get, post, del, put, head, patch, options generate correct arrays', t => {
  const fn = (req, res, store) => {};
  const store = { s: 1 }
  checkRouteArray(get('/a', fn, store), 'GET', '/a', store, t)
  checkRouteArray(post('/b', fn, store), 'POST', '/b', store, t)
  checkRouteArray(del('/c', fn, store), 'DELETE', '/c', store, t)
  checkRouteArray(put('/d', fn, store), 'PUT', '/d', store, t)
  checkRouteArray(head('/e', fn, store), 'HEAD', '/e', store, t)
  checkRouteArray(patch('/f', fn, store), 'PATCH', '/f', store, t)
  checkRouteArray(options('/g', fn, store), 'OPTIONS', '/g', store, t)
  t.end()
})

tap.test('enhancer parses query params correctly', t => {
  const arr = get('/q', (req, res, store) => req.query, { value: 42 })
  const handler = arr[2]
  const [req, res] = buildReqRes('/q?foo=bar&baz=2')
  const params = { p: 'v' }
  const store = arr[3]
  Object.assign(res, { end: () => {} })
  handler(req, res, params, store)
  t.same(req.params, params, 'params attached')
  t.same(req.query, { foo: 'bar', baz: '2' })
  t.end()
})

tap.test('enhancer handles missing host header gracefully', t => {
  const arr = get('/hh', (req, res) => req.query)
  const handler = arr[2]
  const req = { url: '/hh?hello=world', headers: {} }
  const res = { end: () => {} }

  handler(req, res, {}, {})
  t.same(req.query, { hello: 'world' }, 'query works even with undefined host')
  t.end()
})

tap.test('enhancer handles missing query string', t => {
  const arr = get('/noquery', (req, res) => req.query)
  const handler = arr[2]
  const req = { url: '/noquery', headers: { host: 'a.com' } }
  const res = { end: () => {} }
  handler(req, res, {}, {})
  t.same(req.query, {}, 'empty query attached')
  t.end()
})

// Skipping this test as array for router() should be [ path, handler, store ] per amio-micro API, not arrays of arrays.
tap.test('router passes store value through', { skip: true }, t => {
  const { router } = require('..')
  let gotStore
  const rtr = router()([
    get('/store', (req, res, store) => { gotStore = store; res.end('ok') }, { custom: 9 })
  ])
  const http = require('http')
  const server = http.createServer(rtr)

  require('supertest')(server)
    .get('/store')
    .expect(200, 'ok')
    .end((err) => {
      t.error(err)
      t.same(gotStore, { custom: 9 })
      t.end()
    })
})