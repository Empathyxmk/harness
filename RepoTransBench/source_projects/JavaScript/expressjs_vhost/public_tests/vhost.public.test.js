var assert = require('assert')
var http = require('http')
var request = require('supertest')
var vhost = require('../index')

describe('vhost(hostname, server) - PUBLIC', function () {

  it('should route by Host (different public test)', function (done) {
    var vhosts = []

    vhosts.push(vhost('alice.com', alice))
    vhosts.push(vhost('bob.com', bob))

    var app = createServer(vhosts)

    function alice (req, res) { res.end('alice') }
    function bob (req, res) { res.end('bob') }

    request(app)
      .get('/')
      .set('Host', 'bob.com')
      .expect(200, 'bob', done)
  })

  it('should ignore port in Host (public)', function (done) {
    var app = createServer('bob.com', function (req, res) {
      res.end('bob')
    })

    request(app)
      .get('/')
      .set('Host', 'bob.com:1234')
      .expect(200, 'bob', done)
  })

  it('should support another IPv6 literal in Host', function (done) {
    var app = createServer('[::2]', function (req, res) {
      res.end('otherloop')
    })

    request(app)
      .get('/')
      .set('Host', '[::2]:1234')
      .expect(200, 'otherloop', done)
  })

  it('should 404 unless matched (public)', function (done) {
    var vhosts = []

    vhosts.push(vhost('alice.com', alice))
    vhosts.push(vhost('bob.com', bob))

    var app = createServer(vhosts)

    function alice (req, res) { res.end('alice') }
    function bob (req, res) { res.end('bob') }

    request(app)
      .get('/')
      .set('Host', 'cats.com')
      .expect(404, done)
  })

  it('should 404 without Host header (public)', function (done) {
    var vhosts = []

    vhosts.push(vhost('alice.com', alice))
    vhosts.push(vhost('bob.com', bob))

    var server = createServer(vhosts)
    var listeners = server.listeners('request')

    server.removeAllListeners('request')
    listeners.unshift(function (req) { req.headers.host = undefined })
    listeners.forEach(function (l) { server.addListener('request', l) })

    function alice (req, res) { res.end('alice') }
    function bob (req, res) { res.end('bob') }

    request(server)
      .get('/')
      .expect(404, 'no vhost for "undefined"', done)
  })

  describe('arguments', function () {
    describe('hostname', function () {
      it('should be required', function () {
        assert.throws(vhost.bind(), /hostname.*required/)
      })

      it('should accept string', function () {
        assert.doesNotThrow(vhost.bind(null, 'bob.com', function () {}))
      })

      it('should accept RegExp', function () {
        assert.doesNotThrow(vhost.bind(null, /bob\.com/, function () {}))
      })
    })

    describe('handle', function () {
      it('should be required', function () {
        assert.throws(vhost.bind(null, 'bob.com'), /handle.*required/)
      })

      it('should accept function', function () {
        assert.doesNotThrow(vhost.bind(null, 'bob.com', function () {}))
      })

      it('should reject plain object', function () {
        assert.throws(vhost.bind(null, 'bob.com', {}), /handle.*function/)
      })
    })
  })

  describe('with string hostname', function () {
    it('should support wildcards (public)', function (done) {
      var app = createServer('*.cats.com', function (req, res) {
        res.end('meow!')
      })

      request(app)
        .get('/')
        .set('Host', 'fluffy.cats.com')
        .expect(200, 'meow!', done)
    })

    it('should restrict wildcards to single part (public)', function (done) {
      var app = createServer('*.cats.com', function (req, res) {
        res.end('meow!')
      })

      request(app)
        .get('/')
        .set('Host', 'foo.fluffy.cats.com')
        .expect(404, done)
    })

    it('should treat dot as a dot (public)', function (done) {
      var app = createServer('x.y.com', function (req, res) {
        res.end('xyz')
      })

      request(app)
        .get('/')
        .set('Host', 'xXy.com')
        .expect(404, done)
    })

    it('should match entire string (public)', function (done) {
      var app = createServer('.org', function (req, res) {
        res.end('organization')
      })

      request(app)
        .get('/')
        .set('Host', 'foo.org')
        .expect(404, done)
    })

    it('should populate req.vhost (public)', function (done) {
      var app = createServer('client-*.*.org', function (req, res) {
        var keys = Object.keys(req.vhost).sort()
        var arr = keys.map(function (k) { return [k, req.vhost[k]] })
        res.end(JSON.stringify(arr))
      })

      request(app)
        .get('/')
        .set('Host', 'client-alice.bar.org:1234')
        .expect(200, '[["0","alice"],["1","bar"],["host","client-alice.bar.org:1234"],["hostname","client-alice.bar.org"],["length",2]]', done)
    })
  })

  describe('with RegExp hostname', function () {
    it('should match using RegExp (public)', function (done) {
      var app = createServer(/[eh]at\.org/, function (req, res) {
        res.end('hat')
      })

      request(app)
        .get('/')
        .set('Host', 'eat.org')
        .expect(200, 'hat', done)
    })

    it('should match entire hostname (public)', function (done) {
      var vhosts = []

      vhosts.push(vhost(/\.alice$/, alice))
      vhosts.push(vhost(/^bob\./, bob))

      var app = createServer(vhosts)

      function alice (req, res) { res.end('alice') }
      function bob (req, res) { res.end('bob') }

      request(app)
        .get('/')
        .set('Host', 'bob.alice.com')
        .expect(404, done)
    })

    it('should populate req.vhost (public)', function (done) {
      var app = createServer(/client-(alice|sam)\.([^.]+)\.org/, function (req, res) {
        var keys = Object.keys(req.vhost).sort()
        var arr = keys.map(function (k) { return [k, req.vhost[k]] })
        res.end(JSON.stringify(arr))
      })

      request(app)
        .get('/')
        .set('Host', 'client-alice.bar.org:1234')
        .expect(200, '[["0","alice"],["1","bar"],["host","client-alice.bar.org:1234"],["hostname","client-alice.bar.org"],["length",2]]', done)
    })
  })
})

// Copy of test's createServer
function createServer (hostname, server) {
  var vhosts = !Array.isArray(hostname)
    ? [vhost(hostname, server)]
    : hostname

  return http.createServer(function onRequest (req, res) {
    var index = 0

    function next (err) {
      var vhost = vhosts[index++]

      if (!vhost || err) {
        res.statusCode = err ? (err.status || 500) : 404
        res.end(err ? err.message : 'no vhost for "' + req.headers.host + '"')
        return
      }

      vhost(req, res, next)
    }

    next()
  })
}