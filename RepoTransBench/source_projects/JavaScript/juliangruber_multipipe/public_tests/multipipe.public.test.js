/* global describe, it */

const assert = require('assert')
const pipe = require('..')
const Stream = require('stream')
const through = require('through2')

// These versions use different values to transform: 'b' -> 'B' etc.
const ReadableDiff = () => {
  const readable = new Stream.Readable({ objectMode: true })
  readable._read = function () {
    this.push('b')
    this.push(null)
  }
  return readable
}

const TransformDiff = () => {
  const transform = new Stream.Transform({ objectMode: true })
  transform._transform = (chunk, _, done) => {
    done(null, chunk.split('').reverse().join('').toUpperCase()) // e.g. keep 'b', but different transform
  }
  return transform
}

const WritableDiff = cb => {
  const writable = new Stream.Writable({ objectMode: true })
  writable._write = (chunk, _, done) => {
    // Compare with transformed value 'B'
    assert.strictEqual(chunk, 'B')
    done()
    cb && cb()
  }
  return writable
}

describe('public: pipe()', () => {
  it('should return a stream', done => {
    assert(pipe(done))
    done()
  })
  it('should accept options', () => {
    assert.strictEqual(
      pipe({ objectMode: false })._readableState.objectMode,
      false
    )
  })
})

describe('public: pipe(a)', () => {
  it('should pass through to a', done => {
    ReadableDiff()
      .pipe(pipe(TransformDiff()))
      .pipe(WritableDiff(done))
  })
  it('should accept options', () => {
    const readable = ReadableDiff()
    assert.strictEqual(
      pipe(readable, { objectMode: false })._readableState.objectMode,
      false
    )
  })
})

describe('public: pipe(a, b, c)', () => {
  it('should pipe internally', done => {
    pipe(ReadableDiff(), TransformDiff(), WritableDiff(done))
  })

  it('should be writable', done => {
    const stream = pipe(TransformDiff(), WritableDiff(done))
    assert(stream.writable)
    ReadableDiff().pipe(stream)
  })

  it('should be readable', done => {
    const stream = pipe(ReadableDiff(), TransformDiff())
    assert(stream.readable)
    stream.pipe(WritableDiff(done))
  })

  it('should be readable and writable', done => {
    const stream = pipe(TransformDiff(), TransformDiff())
    assert(stream.readable)
    assert(stream.writable)
    ReadableDiff()
      .pipe(stream)
      .pipe(WritableDiff(done))
  })

  describe('errors', () => {
    it('should reemit', done => {
      const a = TransformDiff()
      const b = TransformDiff()
      const c = TransformDiff()
      const stream = pipe(a, b, c)
      const err = new Error('public error')
      let i = 0

      stream.on('error', _err => {
        i++
        assert.strictEqual(_err, err)
        assert(i <= 3)
        if (i === 3) done()
      })

      a.emit('error', err)
      b.emit('error', err)
      c.emit('error', err)
    })

    it('should not reemit endlessly', done => {
      const a = TransformDiff()
      const b = TransformDiff()
      const c = TransformDiff()
      c.readable = false
      const stream = pipe(a, b, c)
      const err = new Error('public error 2')
      let i = 0

      stream.on('error', function (_err) {
        i++
        assert.strictEqual(_err, err)
        assert(i <= 3)
        if (i === 3) done()
      })

      a.emit('error', err)
      b.emit('error', err)
      c.emit('error', err)
    })
  })
  it('should accept options', () => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff()
    assert.strictEqual(
      pipe(a, b, c, { objectMode: false })._readableState.objectMode,
      false
    )
  })
})

describe('public: pipe(a, b, c, fn)', () => {
  it('should call on finish', done => {
    let finished = false
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff(function () {
      finished = true
    })

    pipe(a, b, c, err => {
      assert(!err)
      assert(finished)
      done()
    })
  })

  it('should call with error once', done => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff()
    const err = new Error('error case')

    pipe(a, b, c, err => {
      assert(err)
      done()
    })

    a.emit('error', err)
    b.emit('error', err)
    c.emit('error', err)
  })

  it('should call on destroy', done => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = through()

    pipe(a, b, c, err => {
      assert(!err)
      done()
    })

    c.destroy()
  })

  it('should call on destroy with error', done => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = through()
    const err = new Error('destroy error')

    pipe(a, b, c, _err => {
      assert.strictEqual(_err, err)
      done()
    })

    c.destroy(err)
  })

  it('should accept options', done => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff()
    assert.strictEqual(
      pipe(a, b, c, { objectMode: false }, done)._readableState.objectMode,
      false
    )
    done()
  })

  it('should ignore parameters on non error events', done => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff()
    pipe(a, b, c, done)
    c.emit('finish', 42)
  })
})

describe('public: pipe([a, b, c], fn)', () => {
  it('should call on finish', done => {
    let finished = false
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff(function () {
      finished = true
    })

    pipe([a, b, c], err => {
      assert(!err)
      assert(finished)
      done()
    })
  })
})

describe('public: await pipe(a, b, c)', () => {
  it('should resolve on finish', done => {
    let finished = false
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff(function () {
      finished = true
    })

    pipe(a, b, c).then(() => {
      assert(finished)
      done()
    })
  })

  it('should reject on error', done => {
    const a = ReadableDiff()
    const b = TransformDiff()
    const c = WritableDiff()
    const err = new Error('async error public')

    pipe(a, b, c).catch(_err => {
      assert.strictEqual(_err, err)
      done()
    })

    b.emit('error', err)
  })
})