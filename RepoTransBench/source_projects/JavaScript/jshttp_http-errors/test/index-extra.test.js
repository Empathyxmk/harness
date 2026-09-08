'use strict'

const assert = require('assert')
const createError = require('../index')

// Fix: Remove test that fails due to abstract class restriction
describe('http-errors additional and edge cases', function () {
  it('should throw for unsupported argument type', function () {
    // Pass a symbol as the second argument to trigger the unsupported type branch
    assert.throws(
      () => { createError(404, Symbol('test')) },
      (err) => {
        return (
          err instanceof TypeError &&
          /unsupported type symbol/.test(err.message)
        )
      }
    )
  })

  it('should use default to 500 when given unknown status', function () {
    const err = createError(9999)
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.statusCode, 500)
    assert.strictEqual(err.message, 'Internal Server Error')
  })

  it('should deprecate status below 400', function () {
    // status=200 leads to deprecation, but still works as 200
    const err = createError(200)
    assert.strictEqual(err.status, 200)
    assert.strictEqual(err.statusCode, 200)
    assert.strictEqual(err.message, 'OK')
  })

  it('should create abstract HttpError constructor that cannot be instantiated', function() {
    assert.throws(function () {
      createError.HttpError()
    }, TypeError)
  })

  it('should have constructors for standard status codes as properties', function () {
    const e = new createError.NotFound()
    assert.strictEqual(e.status, 404)
    assert.strictEqual(e.statusCode, 404)
    assert.strictEqual(e.message, 'Not Found')
    assert(e instanceof createError.HttpError)
  });

  it('should not overwrite status/statusCode from props argument', function() {
    const err = createError(404, 'Message', {status: 401, statusCode: 402})
    assert.strictEqual(err.status, 404)
    assert.strictEqual(err.statusCode, 404)
  });

  it('should allow properties through props', function() {
    const err = createError(404, 'foo', {expose: false, custom: true})
    assert.strictEqual(err.message, 'foo')
    assert.strictEqual(err.expose, false)
    assert.strictEqual(err.custom, true)
  });

  describe('createError.isHttpError', function () {
    it('returns false for non-object', function () {
      assert.strictEqual(createError.isHttpError(null), false)
    })
    // Remove test that tries to instantiate the abstract HttpError directly
    it('returns false for plain error', function () {
      assert.strictEqual(createError.isHttpError(new Error('fail')), false)
    })
  })
})