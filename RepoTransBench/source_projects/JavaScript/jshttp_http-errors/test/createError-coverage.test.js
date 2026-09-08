'use strict'

const assert = require('assert')
const createError = require('../index')

// Additional tests for untested branches

describe('http-errors createError function full coverage', function () {
  it('should accept (Error) and preserve existing status', function () {
    const originalError = new Error('original')
    originalError.status = 403
    const err = createError(originalError)
    assert.strictEqual(err.status, 403)
    assert.strictEqual(err.message, 'original')
    assert(err instanceof Error)
  })

  it('should accept (number, string)', function () {
    const err = createError(404, 'Not found')
    assert.strictEqual(err.status, 404)
    assert.strictEqual(err.statusCode, 404)
    assert.strictEqual(err.message, 'Not found')
  })

  it('should accept (number, object)', function () {
    const err = createError(404, { detail: 'something' })
    assert.strictEqual(err.status, 404)
    assert.strictEqual(err.statusCode, 404)
    assert.strictEqual(err.detail, 'something')
  })

  it('should accept (string, object)', function () {
    const err = createError('Custom error', { foo: 1 })
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.statusCode, 500)
    assert.strictEqual(err.foo, 1)
    assert.strictEqual(err.message, 'Custom error')
  })

  it('should accept (number, string, object)', function () {
    const err = createError(400, 'Bad', { detail: 'foo' })
    assert.strictEqual(err.status, 400)
    assert.strictEqual(err.statusCode, 400)
    assert.strictEqual(err.detail, 'foo')
    assert.strictEqual(err.message, 'Bad')
  })

  it('should throw on unsupported type', function () {
    assert.throws(() => createError(400, 123n), /unsupported type bigint/)
  })

  it('should cover non-number status fallback to 500', function () {
    const err = createError({ foo: 'bar' }, 'MyMsg')
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.statusCode, 500)
    assert.strictEqual(err.message, 'MyMsg')
    assert.strictEqual(err.foo, 'bar')
  })

  it('should not add props with forbidden keys', function () {
    const err = createError(404, 'foo', { status: 401, statusCode: 402, x: 1 })
    assert.strictEqual(err.status, 404)
    assert.strictEqual(err.statusCode, 404)
    assert.strictEqual(err.x, 1)
    assert.strictEqual(err.status, err.statusCode)
  })

  it('should create custom error classes via named export', function () {
    const NotFound = createError.NotFound
    const err = new NotFound('Nope')
    assert.strictEqual(err.status, 404)
    assert.strictEqual(err.statusCode, 404)
    assert.strictEqual(err.message, 'Nope')
    assert.strictEqual(err.name, 'NotFoundError')
  })

  it('should expose and name correct properties for client errors', function () {
    const BadRequest = createError.BadRequest
    const err = new BadRequest()
    assert.strictEqual(err.status, 400)
    assert.strictEqual(err.name, 'BadRequestError')
    assert.strictEqual(err.expose, true)
  })

  it('should expose and name correct properties for server errors', function () {
    const InternalServerError = createError.InternalServerError
    const err = new InternalServerError()
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.name, 'InternalServerError')
    assert.strictEqual(err.expose, false)
  })

  it('should use custom error class for specific status codes', function () {
    const err = createError(404)
    assert.strictEqual(err.status, 404)
    assert.strictEqual(err.name, 'NotFoundError')
    assert.strictEqual(err.message, 'Not Found')
  })
})

describe('isHttpError function', () => {
  const isHttpError = createError.isHttpError

  it('should return false for non-objects and null', () => {
    [null, undefined, 0, '', false].forEach(v => {
      assert.strictEqual(isHttpError(v), false)
    })
  })
  it('should return true for instance of HttpError', () => {
    const err = new createError.NotFound()
    assert.strictEqual(isHttpError(err), true)
  })
  it('should return true for generic error with status, statusCode & expose', () => {
    const err = new Error('foo')
    err.status = 410
    err.statusCode = 410
    err.expose = true
    assert.strictEqual(isHttpError(err), true)
  })
  it('should return false for error lacking required shape', () => {
    const err = new Error('bar')
    err.status = 410
    assert.strictEqual(isHttpError(err), false)
  })
})