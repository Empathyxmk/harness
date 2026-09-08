import { describe, it } from 'mocha'
import { Promise, fulfill, reject } from '../src/main'
import { is, assert } from '@briancavalier/assert'
import { rejectsWith } from '../test/lib/test-util'

// Use different test data: numbers and strings, different object instances

describe('Promise (Public)', () => {
  it('should synchronously call resolver', () => {
    let invoked = false
    const p = new Promise((resolve) => {
      invoked = true
      resolve()
    })
    assert(invoked)
    return p
  })

  it('should reject if resolver throws an error synchronously (public)', () => {
    const expectedError = new Error('public error')
    const p = new Promise(() => { throw expectedError })
    return rejectsWith(is(expectedError), p)
  })

  describe('resolvers', () => {
    it('should fulfill with a value (number)', () => {
      const expected = 12345
      return new Promise(resolve => resolve(expected))
        .then(is(expected))
    })

    it('should resolve to a fulfilled promise (string)', () => {
      const expected = 'public fulfilled'
      return new Promise(resolve => resolve(fulfill(expected)))
        .then(is(expected))
    })

    it('should resolve to a rejected promise (Error)', () => {
      const expected = new Error('public rejected')
      const p = new Promise(resolve => resolve(reject(expected)))
      return rejectsWith(is(expected), p)
    })
  })
})