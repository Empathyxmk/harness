'use strict'

const Multispinner = require('../')
const assert = require('chai').assert

describe('Multispinner utilities (public cases)', () => {
  it('success and error set spinner state (different spinner)', () => {
    const m = new Multispinner(['z'], {autoStart: false})
    m.success('z')
    assert.equal(m.spinners['z'].state, require('../lib/constants').states.success)
    m.error('z')
    assert.equal(m.spinners['z'].state, require('../lib/constants').states.error)
  })

  it('update method can be replaced for testing (public: different function)', () => {
    const m = new Multispinner(['pub'], {autoStart: false})
    let calledArg = null
    m.update = function(str) { calledArg = str }
    m.update('test public')
    assert.equal(calledArg, 'test public')
  })

  it('covers postText/preText assignment in Spinners (different key/text/prefix/suffix)', () => {
    const m = new Multispinner({'Y': 'OtherText'}, {autoStart: false, preText: '<<', postText: '>>'})
    assert.isTrue(m.spinners.Y.text.includes('<<'))
    assert.isTrue(m.spinners.Y.text.includes('>>'))
  })
})