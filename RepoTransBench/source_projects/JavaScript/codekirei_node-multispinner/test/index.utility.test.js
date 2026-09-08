'use strict'

const Multispinner = require('../')
const assert = require('chai').assert

describe('Multispinner utilities', () => {
  it('success and error set spinner state', () => {
    const m = new Multispinner(['a'], {autoStart: false})
    m.success('a')
    assert.equal(m.spinners['a'].state, require('../lib/constants').states.success)
    m.error('a')
    assert.equal(m.spinners['a'].state, require('../lib/constants').states.error)
  })

  it('update method can be replaced for testing', () => {
    const m = new Multispinner(['a'], {autoStart: false})
    let logCalled = false
    m.update = function(str) { logCalled = true }
    m.update('hello')
    assert.isTrue(logCalled)
  })

  it('covers postText/preText assignment in Spinners', () => {
    const m = new Multispinner({'X': 'MyText'}, {autoStart: false, preText: 'PRE', postText: 'POST'})
    assert.isTrue(m.spinners.X.text.includes('PRE'))
    assert.isTrue(m.spinners.X.text.includes('POST'))
  })
})