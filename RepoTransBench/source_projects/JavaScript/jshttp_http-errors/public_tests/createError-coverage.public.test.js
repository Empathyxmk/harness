'use strict'

const assert = require('assert')
const createError = require('../index')

// Additional coverage for public tests with different data

describe('http-errors createError function public coverage', function () {
  it('should accept (Error) and preserve existing status (different status)', function () {
    const originalError = new Error('origin')
    originalError.status = 402
    const err = createError(originalError)
    assert.strictEqual(err.status, 402)
    assert.strictEqual(err.message, 'origin')
    assert(err instanceof Error)
  })

  it('should accept (number, string) with different status/message', function () {
    const err = createError(403, 'Forbidden here')
    assert.strictEqual(err.status, 403)
    assert.strictEqual(err.statusCode, 403)
    assert.strictEqual(err.message, 'Forbidden here')
  })

  it('should accept (number, object) with different detail', function () {
    const err = createError(401, { reason: 'denied' })
    assert.strictEqual(err.status, 401)
    assert.strictEqual(err.statusCode, 401)
    assert.strictEqual(err.reason, 'denied')
  })

  it('should accept (string, object) with new string, new object', function () {
    const err = createError('Unique error', { bar: 2 })
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.statusCode, 500)
    assert.strictEqual(err.bar, 2)
    assert.strictEqual(err.message, 'Unique error')
  })

  it('should accept (number, string, object) with different data', function () {
    const err = createError(401, 'No access', { info: 'xyz' })
    assert.strictEqual(err.status, 401)
    assert.strictEqual(err.statusCode, 401)
    assert.strictEqual(err.info, 'xyz')
    assert.strictEqual(err.message, 'No access')
  })

  it('should throw on unsupported type (test for symbol)', function () {
    assert.throws(() => createError(400, Symbol('nope')), /unsupported type symbol/)
  })

  it('should cover non-number status fallback to 500 (different object)', function () {
    const err = createError({ bar: 'baz' }, 'AltMsg')
    assert.strictEqual(err.status, 500)
    assert.strictEqual(err.statusCode, 500)
    assert.strictEqual(err.message, 'AltMsg')
    assert.strictEqual(err.bar, 'baz')
  })

  it('should not add props with forbidden keys, but allow others (different keys)', function () {
    const err = createError(403, 'bar', { status: 200, statusCode: 201, y: 2 })
    assert.strictEqual(err.status, 403)
    assert.strictEqual(err.statusCode, 403)
    assert.strictEqual(err.y, 2)
    assert.strictEqual(err.status, err.statusCode)
  })

  it('should create custom error classes via another named export (Gone)', function () {
    const Gone = createError.Gone
    const err = new Gone('No longer here')
    assert.strictEqual(err.status, 410)
    assert.strictEqual(err.statusCode, 410)
    assert.strictEqual(err.message, 'No longer here')
    assert.strictEqual(err.name, 'GoneError')
  })

  it('should expose and name correct properties for different client error (Unauthorized)', function () {
    const Unauthorized = createError.Unauthorized
    const err = new Unauthorized()
    assert.strictEqual(err.status, 401)
    assert.strictEqual(err.name, 'UnauthorizedError')
    assert.strictEqual(err.expose, true)
  })

  it('should expose and name correct properties for different server error (BadGateway)', function () {
    const BadGateway = createError.BadGateway
    const err = new BadGateway()
    assert.strictEqual(err.status, 502)
    assert.strictEqual(err.name, 'BadGatewayError')
    assert.strictEqual(err.expose, false)
  })

  it('should use custom error class for another specific status code', function () {
    const err = createError(401)
    assert.strictEqual(err.status, 401)
    assert.strictEqual(err.name, 'UnauthorizedError')
    assert.strictEqual(err.message, 'Unauthorized')
  })
})

describe('isHttpError function (public)', () => {
  const isHttpError = createError.isHttpError

  it('should return false for different non-objects and null', () => {
    [undefined, NaN, 1, 'hello', true].forEach(v => {
      assert.strictEqual(isHttpError(v), false)
    })
  })
  it('should return true for instance of another HttpError type', () => {
    const err = new createError.Gone()
    assert.strictEqual(isHttpError(err), true)
  })
  it('should return true for different generic error with status, statusCode & expose', () => {
    const err = new Error('bar')
    err.status = 418
    err.statusCode = 418
    err.expose = true
    assert.strictEqual(isHttpError(err), true)
  })
  it('should return false for error lacking expose', () => {
    const err = new Error('baz')
    err.status = 418
    err.statusCode = 418
    assert.strictEqual(isHttpError(err), false)
  })
})