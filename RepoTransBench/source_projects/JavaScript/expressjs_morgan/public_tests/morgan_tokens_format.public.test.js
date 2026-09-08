const morgan = require('../index');
const http = require('http');

describe('morgan tokens/format (public)', () => {
  test('should define a different custom token and use it in format', done => {
    morgan.token('customPubToken', (req, res) => 'xyz_987');
    morgan.format('customPubFormat', ':method :url :customPubToken');
    const logs = [];
    const mw = morgan('customPubFormat', {
      stream: {
        write(str) {
          logs.push(str);
        }
      }
    });

    const req = new http.IncomingMessage();
    req.method = 'OPTIONS';
    req.url = '/pubtokentest';
    req.connection = { remoteAddress: '9.8.7.6' };
    const res = new http.ServerResponse(req);

    mw(req, res, () => {
      res.statusCode = 202;
      res.end();
      res.emit('finish');
      setTimeout(() => {
        expect(logs.join('')).toContain('OPTIONS /pubtokentest xyz_987');
        done();
      }, 20);
    });
  });

  test('should skip logging if public token returns undefined (simulate)', done => {
    morgan.token('puberrtoken', () => undefined);
    morgan.format('puberrFormat', ':method :url :puberrtoken');
    const logs = [];
    const stream = { write: (x) => logs.push(x) };
    const mw = morgan('puberrFormat', { stream, skip: () => false });

    const req = new http.IncomingMessage();
    req.method = 'DELETE';
    req.url = '/puberrtest';
    req.connection = { remoteAddress: '1.1.1.1' };
    const res = new http.ServerResponse(req);
    let reached = false;

    mw(req, res, () => {
      res.statusCode = 410;
      try { res.end(); } catch (e) {}
      res.emit('finish');
      reached = true;
      setTimeout(() => {
        expect(reached).toBe(true);
        // The expected log is: "DELETE /puberrtest -\n"
        expect(logs.join('')).toContain('DELETE /puberrtest -');
        done();
      }, 10);
    });
  });

  test('should allow defining and deleting another custom format and token', () => {
    morgan.format('to_remove_pub', ':method :url :random');
    morgan.token('to_remove_pub_token', () => 'another');

    expect(typeof morgan.format).toBe('function');
    expect(typeof morgan.token).toBe('function');
    morgan.format('to_remove_pub', undefined);
    morgan.token('to_remove_pub_token', undefined);
    let threw = false;
    try {
      morgan('to_remove_pub');
    } catch (e) {
      threw = true;
    }
    expect(threw).toBe(false);
  });

  test('should allow function predicate as skip (public)', done => {
    const mw = morgan('tiny', {
      skip(req) { return req.url === '/publicshouldskip'; },
      stream: { write: () => { throw new Error('should not call'); } }
    });
    const req = new http.IncomingMessage();
    req.method = 'HEAD'; req.url = '/publicshouldskip';
    req.connection = { remoteAddress: '12.34.56.78' };
    const res = new http.ServerResponse(req);
    mw(req, res, () => {
      res.emit('finish');
      setTimeout(() => { done(); }, 5);
    });
  });

  test('should check default formats: combined, common, dev, short, tiny (public)', () => {
    ['combined', 'common', 'dev', 'short', 'tiny'].forEach(name => {
      expect(() => morgan(name)).not.toThrow();
    });
  });
});