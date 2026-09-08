import { describe, it } from 'mocha'
import { is, assert } from '@briancavalier/assert'
import Action from '../src/Action'

// Use different data for objects and new property names

describe('Action (Public)', () => {
  it('should expose promise and context', () => {
    const customPromise = { publicId: 88 }
    const action = new Action(customPromise)

    is(customPromise, action.promise)
    assert('context' in action)
  })

  describe('fulfilled', () => {
    it('should set actual to incoming fulfilled value', () => {
      const different = { pass: 'ok' }
      const promise = {
        actual: undefined,
        _become (p) {
          this.actual = p
        }
      }
      const action = new Action(promise)
      action.fulfilled(different)
      is(different, promise.actual)
    })
  })

  describe('rejected', () => {
    it('should set actual to incoming rejected value', () => {
      const another = { reject: 99 }
      const promise = {
        actual: undefined,
        _become (p) {
          this.actual = p
        }
      }
      const action = new Action(promise)
      action.rejected(another)
      is(another, promise.actual)
    })
  })
})