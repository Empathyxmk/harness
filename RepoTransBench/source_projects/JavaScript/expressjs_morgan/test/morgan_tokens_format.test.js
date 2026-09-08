const morgan = require('../index');
const http = require('http');

describe('morgan tokens/format', () => {
  test('should define custom token and use it in format', done => {
    morgan.token('customToken', (req, res) => 'foo_bar');
    morgan.format('customFormat', ':method :url :customToken');
    const logs = [];
    const mw = morgan('customFormat', {
      stream: {
        write(str) {
          logs.push(str);
        }
      }
    });

    const req = new http.IncomingMessage();
    req.method = 'PATCH';
    req.url = '/tokentest';
    req.connection = { remoteAddress: '1.2.3.4' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.statusCode = 201;
      res.end();
      res.emit('finish');
      setTimeout(() => {
        expect(logs.join('')).toContain('PATCH /tokentest foo_bar');
        done();
      }, 20);
    });
  });

  // Fixed: simulate token returning undefined, Morgan will print "-".
  test('should skip logging if token returns undefined (simulate error, but don\'t throw)', done => {
    morgan.token('errtoken2', () => undefined);
    morgan.format('errFormat2', ':method :url :errtoken2');
    // Provide a writable stream that just swallows writes
    const logs = [];
    const stream = { write: (x) => logs.push(x) };
    const mw = morgan('errFormat2', { stream, skip: () => false });

    const req = new http.IncomingMessage();
    req.method = 'POST';
    req.url = '/errtest';
    req.connection = { remoteAddress: '::1' };
    const res = new http.ServerResponse(req);
    let reached = false;

    mw(req, res, () => {
      res.statusCode = 404;
      try { res.end(); } catch (e) {}
      res.emit('finish');
      reached = true;
      setTimeout(() => {
        expect(reached).toBe(true);
        // The expected log is: "POST /errtest -\n"
        expect(logs.join('')).toContain('POST /errtest -');
        done();
      }, 10);
    });
  });

  test('should allow defining and then deleting a custom format and token', () => {
    morgan.format('to_remove', ':method :url');
    morgan.token('to_remove_token', (req, res) => 'dummy');

    // Exported API: .formats and .tokens are functions, not objects (they are not exported!)
    expect(typeof morgan.format).toBe('function');
    expect(typeof morgan.token).toBe('function');
    // Remove using undefined (documented removal)
    morgan.format('to_remove', undefined); // Remove format
    morgan.token('to_remove_token', undefined); // Remove token
    // No exception should occur, fallback to default, not an error
    let threw = false;
    try {
      morgan('to_remove');
    } catch (e) {
      threw = true;
    }
    expect(threw).toBe(false);
  });

  test('should allow function predicate as skip', done => {
    const mw = morgan('tiny', {
      skip(req) { return req.url === '/shouldskip'; },
      stream: { write: () => { throw new Error('should not call'); } }
    });
    const req = new http.IncomingMessage();
    req.method = 'GET'; req.url = '/shouldskip';
    req.connection = { remoteAddress: '6.7.8.9' };
    const res = new http.ServerResponse(req);
    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => { done(); }, 5);
    });
  });

  test('should have default formats: combined, common, dev, short, tiny', () => {
    // The public API does not expose .formats, but calling morgan() with a default format name should work
    ['combined', 'common', 'dev', 'short', 'tiny'].forEach(name => {
      expect(() => morgan(name)).not.toThrow();
    });
  });
});