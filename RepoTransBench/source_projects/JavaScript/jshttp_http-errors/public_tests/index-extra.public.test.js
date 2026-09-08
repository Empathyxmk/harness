'use strict'

const assert = require('assert')
const createError = require('../index')

// Public: additional and edge cases with different data
describe('http-errors public additional and edge cases', function () {
  it('should throw for unsupported argument type (test for bigint)', function () {
    // Pass a bigint as the second argument
    assert.throws(
      () => { createError(400, 10n) },
      (err) => {
        return (
          err instanceof TypeError &&
          /unsupported type bigint/.test(err.message)
        )
      }
    )
  })

  it('should use default to 500 when given another unknown status', function () {
    const err = createError(12345)
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.statusCode, 500)
    assert.strictEqual(err.message, 'Internal Server Error')
  })

  it('should deprecate status below 400 (status=304)', function () {
    // status=304 ("Not Modified") is below 400
    const err = createError(304)
    assert.strictEqual(err.status, 304)
    assert.strictEqual(err.statusCode, 304)
    assert.strictEqual(err.message, 'Not Modified')
  })

  it('should create abstract HttpError constructor that cannot be instantiated (public)', function() {
    assert.throws(function () {
      createError.HttpError()
    }, TypeError)
  })

  it('should have constructors for standard status codes as properties (Gone)', function () {
    const e = new createError.Gone()
    assert.strictEqual(e.status, 410)
    assert.strictEqual(e.statusCode, 410)
    assert.strictEqual(e.message, 'Gone')
    assert(e instanceof createError.HttpError)
  });

  it('should not overwrite status/statusCode from props argument (Gone)', function() {
    const err = createError(410, 'Other Message', {status: 412, statusCode: 413})
    assert.strictEqual(err.status, 410)
    assert.strictEqual(err.statusCode, 410)
  });

  it('should allow properties through props (allow info, extra)', function() {
    const err = createError(401, 'oops', {expose: true, info: 'extra'})
    assert.strictEqual(err.message, 'oops')
    assert.strictEqual(err.expose, true)
    assert.strictEqual(err.info, 'extra')
  });

  describe('createError.isHttpError (public)', function () {
    it('returns false for undefined', function () {
      assert.strictEqual(createError.isHttpError(undefined), false)
    })
    it('returns false for generic object', function () {
      assert.strictEqual(createError.isHttpError({}), false)
    })
    it('returns false for error with only statusCode', function () {
      const err = new Error('fail')
      err.statusCode = 404
      assert.strictEqual(createError.isHttpError(err), false)
    })
  })
})