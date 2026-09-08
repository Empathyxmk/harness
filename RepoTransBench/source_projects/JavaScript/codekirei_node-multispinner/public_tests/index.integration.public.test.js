'use strict'

// Integration + edge & event tests for Multispinner (public cases)
const Multispinner = require('../')
const assert = require('chai').assert
const sinon = require('sinon')

describe('Multispinner integration/edge (public cases)', () => {
  const PUB_SPINNERS = ['alpha', 'beta', 'gamma']

  it('autoStart starts loop and triggers events on success (public spinners)', function(done) {
    // stub update, setTimeout
    const clock = sinon.useFakeTimers()
    const update = sinon.stub()
    update.clear = sinon.stub()
    update.done = sinon.stub()
    const opts = {
      interval: 2,
      autoStart: true
    }
    const m = new Multispinner(PUB_SPINNERS, opts)
    m.update = update

    let events = []
    m.on('done', () => { events.push('done') })
    m.on('success', () => { events.push('success') })
    m.on('err', () => { events.push('err') })

    // success all spinners
    PUB_SPINNERS.forEach(s => m.success(s))

    // advance timers so loop completes
    clock.tick(20)

    setTimeout(() => {
      assert.deepEqual(events, ['done', 'success'])
      done()
      clock.restore()
    }, 0)
    clock.tick(1)
  })

  it('autoStart triggers err events if any error (public different error)', function(done) {
    const clock = sinon.useFakeTimers()
    const update = sinon.stub()
    update.clear = sinon.stub()
    update.done = sinon.stub()
    const opts = {
      interval: 2,
      autoStart: true
    }
    const m = new Multispinner(PUB_SPINNERS, opts)
    m.update = update

    let errorEvents = []
    m.on('done', () => errorEvents.push('done'))
    m.on('success', () => errorEvents.push('success'))
    m.on('err', (spinner) => errorEvents.push('err:' + spinner))

    // Public: error on "beta", others success
    m.success('alpha')
    m.error('beta')
    m.success('gamma')

    clock.tick(20)

    setTimeout(() => {
      assert.includeMembers(errorEvents, ['done', 'err:beta'])
      assert.notInclude(errorEvents, 'success') // there was an error
      done()
      clock.restore()
    }, 0)
    clock.tick(1)
  })

  it('loop handles update.clear undefined safely (public case)', function() {
    const clock = sinon.useFakeTimers()
    const m = new Multispinner(['u'], {autoStart: false, interval: 2})
    let called = false
    m.update = function(str) { called = true }
    // no clear function
    m.update.done = function(){}
    m.success('u')
    // triggers loop with update.clear undefined
    m.loop()
    clock.tick(2)
    clock.restore()
    assert(called)
  })

  it('constructor should support custom frames and indent (public different frames/indent)', function() {
    const spinners = ['unique']
    const opts = {
      autoStart: false,
      indent: 3,
      frames: ['*','-','#'],
      preText: '***',
      postText: '###',
    }
    const m = new Multispinner(spinners, opts)
    assert.equal(m.frames.length, 3)
    assert.equal(m.indentStr, '   ')
  })

  it('should allow spinners to be input as object (public - key/value different)', function() {
    const m = new Multispinner({pubSpin: 'otherPublic'}, {autoStart: false})
    assert.isObject(m.spinners)
    assert.property(m.spinners, 'pubSpin')
  })
})