const morgan = require('../index');
const http = require('http');
const stream = require('stream');

describe('morgan main export (public)', () => {
  test('should export morgan as a function (public)', () => {
    expect(typeof morgan).toBe('function');
  });

  test('should expose compile, format, token (public)', () => {
    expect(typeof morgan.compile).toBe('function');
    expect(typeof morgan.format).toBe('function');
    expect(typeof morgan.token).toBe('function');
  });

  test('should return middleware function (public)', () => {
    const mw = morgan('common');
    expect(typeof mw).toBe('function');
    expect(mw.length >= 3).toBe(true);
  });

  test('should handle options object as first param (different format)', done => {
    let emitted = '';
    const writable = new stream.Writable({
      write(chunk, encoding, callback) {
        emitted += chunk.toString();
        callback();
      }
    });
    const mw = morgan({ format: 'short', stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'HEAD'; req.url = '/public/';
    req.connection = { remoteAddress: '192.168.100.2' };
    const res = new http.ServerResponse(req);
    let calledNext = false;
    mw(req, res, () => { calledNext = true; res.statusCode = 203; res.end(); });
    res.emit('finish');
    setTimeout(() => {
      expect(emitted).toContain('HEAD /public/ 203');
      expect(calledNext).toBe(true);
      done();
    }, 10);
  });

  test('should accept format function (public)', done => {
    let output = '';
    const writable = new stream.Writable({
      write(chunk, encoding, cb) { output += chunk; cb(); }
    });
    const mw = morgan((tokens, req, res) => 'public-log-string', { stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'CONNECT';
    req.url = '/bar';
    req.connection = { remoteAddress: '172.16.0.3' };
    const res = new http.ServerResponse(req);
    mw(req, res, () => { res.end(); res.emit('finish'); });

    setTimeout(() => {
      expect(output).toContain('public-log-string');
      done();
    }, 20);
  });

  test('should call skip if present and skip (public returns true)', done => {
    let calledSkip = false;
    const mw = morgan('short', {
      skip(req, res) {
        calledSkip = true;
        return true;
      },
      stream: { write: () => { throw new Error('should not call stream.write'); } }
    });
    const req = new http.IncomingMessage();
    req.method = 'PATCH';
    req.url = '/pqr';
    req.connection = { remoteAddress: '192.0.2.10' };
    const res = new http.ServerResponse(req);
    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(calledSkip).toBe(true);
        done();
      }, 10);
    });
  });

  test('should call stream.write with new line and starts with correct string (public)', done => {
    let written = '';
    const writable = new stream.Writable({
      write(chunk, encoding, cb) { written += chunk; cb(); }
    });
    const mw = morgan('short', { stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'DELETE'; req.url = '/publicwrite';
    req.connection = { remoteAddress: '203.0.113.5' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(written.endsWith('\n')).toBe(true);
        expect(written.startsWith('DELETE /publicwrite')).toBe(true);
        done();
      }, 15);
    });
  });

  test('should buffer log when buffer option is used (public)', done => {
    let flushed = '';
    const writable = new stream.Writable({
      write(chunk, _, cb) { flushed += chunk; cb(); }
    });
    const mw = morgan('combined', { buffer: 70, stream: writable });
    const req = new http.IncomingMessage();
    req.method = 'PUT';
    req.url = '/bufferedpub';
    req.connection = { remoteAddress: '8.8.8.8' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => {
        expect(flushed.length).toBeGreaterThan(0);
        done();
      }, 200);
    });
  });

  test('should immediate: true log on middleware call (public)', done => {
    let str = '';
    const writable = new stream.Writable({
      write(chunk, _, cb) { str += chunk; cb(); }
    });
    const mw = morgan('tiny', { stream: writable, immediate: true });
    const req = new http.IncomingMessage();
    req.method = 'HEAD';
    req.url = '/immediatepub';
    req.connection = { remoteAddress: '198.51.100.77' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      expect(str).toContain('HEAD /immediatepub');
      done();
    });
  });

  test('should handle undefined format gracefully (public)', () => {
    expect(() => morgan(undefined, { stream: { write: () => {} }})).not.toThrow();
  });

  test('should support options.skip as false (public)', done => {
    let called = false;
    const mw = morgan('dev', { skip: false, stream: { write: () => { called = true; } } });
    const req = new http.IncomingMessage();
    req.method = 'PATCH';
    req.url = '/publicfalse';
    req.connection = { remoteAddress: '150.150.150.150' };
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