'use strict'

// Integration + edge & event tests for Multispinner
const Multispinner = require('../')
const assert = require('chai').assert
const sinon = require('sinon')

describe('Multispinner integration/edge', () => {
  const SPINNERS = ['a', 'b', 'c']

  it('autoStart starts loop and triggers events on success', function(done) {
    // stub update, setTimeout
    const clock = sinon.useFakeTimers()
    const update = sinon.stub()
    update.clear = sinon.stub()
    update.done = sinon.stub()
    const opts = {
      interval: 1,
      autoStart: true
    }
    const m = new Multispinner(SPINNERS, opts)
    m.update = update

    let events = []
    m.on('done', () => { events.push('done') })
    m.on('success', () => { events.push('success') })
    m.on('err', () => { events.push('err') })

    // success all spinners
    SPINNERS.forEach(s => m.success(s))

    // advance timers so loop completes
    clock.tick(10)

    // Loop async - after one event loop tick, events should have fired
    setTimeout(() => {
      assert.deepEqual(events, ['done', 'success'])
      done()
      clock.restore()
    }, 0)
    clock.tick(1)
  })

  it('autoStart triggers err events if any error', function(done) {
    const clock = sinon.useFakeTimers()
    const update = sinon.stub()
    update.clear = sinon.stub()
    update.done = sinon.stub()
    const opts = {
      interval: 1,
      autoStart: true
    }
    const m = new Multispinner(SPINNERS, opts)
    m.update = update

    let errorEvents = []
    m.on('done', () => errorEvents.push('done'))
    m.on('success', () => errorEvents.push('success'))
    m.on('err', (spinner) => errorEvents.push('err:' + spinner))

    // complete: 1 error, rest success
    m.success('a')
    m.error('b')
    m.success('c')

    clock.tick(10)

    setTimeout(() => {
      assert.includeMembers(errorEvents, ['done', 'err:b'])
      assert.notInclude(errorEvents, 'success') // there was an error
      done()
      clock.restore()
    }, 0)
    clock.tick(1)
  })

  it('loop handles update.clear undefined safely', function() {
    const clock = sinon.useFakeTimers()
    const m = new Multispinner(['x'], {autoStart: false, interval: 1})
    let updated = false
    m.update = function(str) { updated = true }
    // no clear function
    m.update.done = function(){}
    m.success('x')
    // triggers loop with update.clear undefined
    m.loop()
    clock.tick(1)
    clock.restore()
    assert(updated)
  })

  it('constructor should support custom frames and indent', function() {
    const spinners = ['foo']
    const opts = {
      autoStart: false,
      indent: 5,
      frames: ['.','o'],
      preText: '',
      postText: '',
    }
    const m = new Multispinner(spinners, opts)
    assert.equal(m.frames.length, 2)
    assert.equal(m.indentStr, '     ')
  })

  it('should allow spinners to be input as object', function() {
    const m = new Multispinner({spin1: 'text'}, {autoStart: false})
    assert.isObject(m.spinners)
    assert.property(m.spinners, 'spin1')
  })
})