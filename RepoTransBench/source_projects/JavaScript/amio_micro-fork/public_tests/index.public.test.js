const tap = require('tap')
const request = require('supertest')
const { router, get, put, del, post, head, patch, options } = require('..')

const pubServer = require('http').createServer(router()(
  get('/pong', (req, res) => res.end('ping')),
  post('/items', (req, res) => res.end('item created')),
  del('/items/:uuid', (req, res) => res.end(`removed ${req.params.uuid}`)),
  get('/items', (req, res) => res.end(`query type ${req.query.type}`))
))

tap.test('Exports right api types [public]', t => {
  t.equal(typeof router, 'function', 'exports function router')
  t.equal(typeof get, 'function', 'exports function get')
  t.equal(typeof put, 'function', 'exports function put')
  t.equal(typeof del, 'function', 'exports function del')
  t.equal(typeof post, 'function', 'exports function post')
  t.equal(typeof head, 'function', 'exports function head')
  t.equal(typeof patch, 'function', 'exports function patch')
  t.equal(typeof options, 'function', 'exports function options')
  t.end()
})

tap.test('Response to GET:/pong with 200 [public]', t => {
  return request(pubServer)
    .get('/pong')
    .expect(200, 'ping')
})

tap.test('Response to POST:/items with 200 [public]', t => {
  return request(pubServer)
    .post('/items')
    .send({ type: 'tool' })
    .expect(200, 'item created')
})

tap.test('Response to DELETE:/items/abc-789 with 200 [public]', t => {
  return request(pubServer)
    .delete('/items/abc-789')
    .expect(200, 'removed abc-789')
})

tap.test('Response to GET:/items?type=gadget with 200 [public]', t => {
  return request(pubServer)
    .get('/items?type=gadget')
    .expect(200, 'query type gadget')
})

tap.test('Response to unmatched route with 404 [public]', t => {
  return request(pubServer)
    .get('/notfound')
    .expect(404)
})