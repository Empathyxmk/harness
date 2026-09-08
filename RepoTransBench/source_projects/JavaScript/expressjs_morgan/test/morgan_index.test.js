const morgan = require('../index');
const http = require('http');
const stream = require('stream');

describe('morgan main export', () => {
  test('should export morgan as a function', () => {
    expect(typeof morgan).toBe('function');
  });

  test('should expose compile, format, token', () => {
    expect(typeof morgan.compile).toBe('function');
    expect(typeof morgan.format).toBe('function');
    expect(typeof morgan.token).toBe('function');
  });

  test('should return middleware function', () => {
    const mw = morgan('dev');
    expect(typeof mw).toBe('function');
    expect(mw.length >= 3).toBe(true); // req, res, next
  });

  test('should handle options object as first param (backcompat)', done => {
    let emitted = '';
    const writable = new stream.Writable({
      write(chunk, encoding, callback) {
        emitted += chunk.toString();
        callback();
      }
    });
    const mw = morgan({ format: 'tiny', stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'GET'; req.url = '/'; req.connection = { remoteAddress: '127.0.0.1' };
    const res = new http.ServerResponse(req);
    let calledNext = false;
    mw(req, res, () => { calledNext = true; res.statusCode = 200; res.end(); });
    res.emit('finish');
    setTimeout(() => {
      expect(emitted).toContain('GET / 200');
      expect(calledNext).toBe(true);
      done();
    }, 10);
  });

  test('should accept format function', done => {
    let output = '';
    const writable = new stream.Writable({
      write(chunk, encoding, cb) { output += chunk; cb(); }
    });
    const mw = morgan((tokens, req, res) => 'custom-log', { stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'POST';
    req.url = '/foo';
    req.connection = { remoteAddress: '10.0.0.2' };
    const res = new http.ServerResponse(req);
    mw(req, res, () => { res.end(); res.emit('finish'); });

    setTimeout(() => {
      expect(output).toContain('custom-log');
      done();
    }, 20);
  });

  test('should call skip if present and skip (returns true)', done => {
    let calledSkip = false;
    const mw = morgan('tiny', {
      skip(req, res) {
        calledSkip = true;
        return true;
      },
      stream: { write: () => { throw new Error('should not call stream.write'); } }
    });
    const req = new http.IncomingMessage();
    req.method = 'GET';
    req.url = '/abc';
    req.connection = { remoteAddress: '::1' };
    const res = new http.ServerResponse(req);
    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(calledSkip).toBe(true);
        done();
      }, 10);
    });
  });

  test('should call stream.write with new line', done => {
    let written = '';
    const writable = new stream.Writable({
      write(chunk, encoding, cb) { written += chunk; cb(); }
    });
    const mw = morgan('tiny', { stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'PUT'; req.url = '/write';
    req.connection = { remoteAddress: '::2' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(written.endsWith('\n')).toBe(true);
        expect(written.startsWith('PUT /write')).toBe(true);
        done();
      }, 15);
    });
  });

  test('should buffer log when buffer option is truthy', done => {
    let flushed = '';
    const writable = new stream.Writable({
      write(chunk, _, cb) { flushed += chunk; cb(); }
    });
    // buffer: 100 (ms) so we flush soon
    const mw = morgan('common', { buffer: 100, stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'GET';
    req.url = '/buffered';
    req.connection = { remoteAddress: '127.0.0.13' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(flushed.length).toBeGreaterThan(0);
        done();
      }, 200);
    });
  });

  test('should immediate: true log on middleware call', done => {
    let str = '';
    const writable = new stream.Writable({
      write(chunk, _, cb) { str += chunk; cb(); }
    });
    const mw = morgan('dev', { stream: writable, immediate: true });
    const req = new http.IncomingMessage();
    req.method = 'GET';
    req.url = '/immediate';
    req.connection = { remoteAddress: '127.0.0.22' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      expect(str).toContain('GET /immediate');
      done();
    });
  });

  test('should handle undefined format gracefully', () => {
    // Should not throw, triggers deprecation
    expect(() => morgan(undefined, { stream: { write: () => {} }})).not.toThrow();
  });

  test('should support options.skip as false', done => {
    let called = false;
    const mw = morgan('common', { skip: false, stream: { write: () => { called = true; } } });
    const req = new http.IncomingMessage();
    req.method = 'POST';
    req.url = '/false';
    req.connection = { remoteAddress: '127.0.0.5' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(called).toBe(true);
        done();
      }, 20);
    });
  });

});