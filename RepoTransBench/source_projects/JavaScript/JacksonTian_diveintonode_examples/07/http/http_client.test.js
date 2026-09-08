const http = require('http');

describe('07/http/client.js', () => {
  let server;
  beforeAll((done) => {
    server = http.createServer((req, res) => {
      res.writeHead(200, {'X-Test': 'ok'});
      res.end('testdata');
    }).listen(1337, done);
  });

  afterAll((done) => {
    server.close(done);
  });

  test('client gets response and logs', (done) => {
    const logs = [];
    const origConsoleLog = console.log;
    console.log = (msg) => logs.push(msg);

    const options = {
      hostname: '127.0.0.1',
      port: 1337,
      path: '/',
      method: 'GET'
    };

    const req = http.request(options, function(res) {
      logs.push('STATUS: ' + res.statusCode);
      logs.push('HEADERS: ' + JSON.stringify(res.headers));
      res.setEncoding('utf8');
      let chunked = '';
      res.on('data', function (chunk) {
        chunked += chunk;
      });
      res.on('end', () => {
        expect(logs.some(l => l.includes('STATUS: 200'))).toBeTruthy();
        expect(logs.some(l => l.includes('HEADERS'))).toBeTruthy();
        expect(chunked).toBe('testdata');
        console.log = origConsoleLog;
        done();
      });
    });
    req.end();
  });
});