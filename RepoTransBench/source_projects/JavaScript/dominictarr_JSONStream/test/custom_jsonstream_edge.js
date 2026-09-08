var JSONStream = require('../')
var it = require('it-is')
var Stream = require('stream').Stream

// parse emits error on invalid JSON
exports['parse emits error on invalid JSON'] = function (test) {
  var parse = JSONStream.parse()
  var gotError = false

  parse.on('error', function (err) {
    gotError = true
    test && test.ok && test.ok(err instanceof Error, 'error event received')
    // End here so test will not timeout
    if (typeof test.end === 'function') test.end()
  })

  // Write invalid json, should error
  parse.write('{"id":1')
  setTimeout(function () {
    if (!gotError) {
      if (test && test.fail) test.fail('error event not emitted')
      if (typeof test.end === 'function') test.end()
    }
  }, 100)
}

// parse emits root object when no path is provided
exports['parse emits root object when no path is provided'] = function (test) {
  var parse = JSONStream.parse()
  var obj
  parse.on('data', function (_obj) { obj = _obj })
  parse.on('end', function () {
    it(obj)
      .deepEqual({foo:"bar"})
    test && test.ok && test.ok(true, 'root object emitted')
    if (typeof test.end === 'function') test.end()
  })
  parse.end('{"foo":"bar"}')
}

// parse emits header/footer for unexpected keys
exports['parse emits header/footer for wrong path'] = function (test) {
  var headerEmitted = false, footerEmitted = false
  var parse = JSONStream.parse('docs.*')
  parse.on('header', function (h) {
    headerEmitted = true
    it(h.rows).equal(undefined)
  })
  parse.on('footer', function (f) {
    footerEmitted = true
    it(f).deepEqual([])
  })
  parse.on('error', function (err) {}) // ignore errors
  parse.end('{"rows":[{"id":1}],"docs":[{"id":2}]}')
  setTimeout(function () {
    test && test.ok && test.ok(headerEmitted && footerEmitted, 'emits header/footer for wrong path')
    if (typeof test.end === 'function') test.end()
  }, 20)
}

// parse with map function returning null skips output
exports['parse with map function returning null skips output'] = function (test) {
  var parse = JSONStream.parse('rows.*', function (row) {
    if (row.skip) return null
    return row
  })
  var cnt = 0
  parse.on('data', function (row) { cnt++ })
  parse.on('end', function () {
    it(cnt).equal(1)
    test && test.ok && test.ok(true, 'only one output with map')
    if (typeof test.end === 'function') test.end()
  })
  parse.end('{"rows":[{"val":1},{"skip":true}]}')
}

// should be equivalent
exports['should be equivalent'] = function (test) {
  var parse = JSONStream.parse('rows.*')
  var expected = [{val:1},{val:2}]
  var actual = []
  parse.on('data', function (row) { actual.push(row) })
  parse.on('end', function () {
    it(actual).deepEqual(expected)
    test && test.ok && test.ok(true, 'should be equivalent')
    if (typeof test.end === 'function') test.end()
  })
  parse.end('{"rows":[{"val":1},{"val":2}]}')
}

// stringify numbers works
exports['stringify numbers works'] = function (test) {
  var s = JSONStream.stringify()
  var data = ''
  s.on('data', function (d) { data += d })
  s.on('end', function () {
    it(data).equal('[1]')
    test && test.ok && test.ok(true, 'stringify numbers works')
    if (typeof test.end === 'function') test.end()
  })
  s.write(1)
  s.end()
}

// output is empty array
exports['output is empty array'] = function (test) {
  var s = JSONStream.stringify()
  var data = ''
  s.on('data', function (d) { data += d })
  s.on('end', function () {
    it(data).equal('[]')
    test && test.ok && test.ok(true, 'output is empty array')
    if (typeof test.end === 'function') test.end()
  })
  s.end()
}

// should be equivalent with recurse/regex
exports['should be equivalent with recurse/regex'] = function (test) {
  var parse = JSONStream.parse('$..*')
  var objects = []
  parse.on('data', function (obj) { objects.push(obj) })
  parse.on('end', function () {
    it(objects.length).ok('should be equivalent')
    test && test.ok && test.ok(true, 'should be equivalent')
    if (typeof test.end === 'function') test.end()
  })
  parse.end(JSON.stringify({"foo":1,"bar":{"baz":2}}))
}

// should be equal for emitKey/emitPath objects as path
exports['should be equal for emitKey/emitPath objects as path'] = function (test) {
  var parse = JSONStream.parse({emitKey: true, path: 'a.b'})
  var objects = []
  parse.on('data', function (obj) { objects.push(obj) })
  parse.on('end', function () {
    it(objects.length).equal(0)
    test && test.ok && test.ok(true, 'should be equal')
    if (typeof test.end === 'function') test.end()
  })
  parse.end(JSON.stringify({"foo":1,"bar":{"baz":2}}))
}

// should be equivalent emitKey/emitPath
exports['should be equivalent emitKey/emitPath'] = function (test) {
  var parse = JSONStream.parse({emitKey: true, path: '*'})
  var objects = []
  parse.on('data', function (obj) { objects.push(obj) })
  parse.on('end', function () {
    it(objects.length).ok('should be equivalent')
    test && test.ok && test.ok(true, 'should be equivalent')
    if (typeof test.end === 'function') test.end()
  })
  parse.end(JSON.stringify({"foo":1,"bar":{"baz":2}}))
}