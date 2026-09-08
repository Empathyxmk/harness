const http = require('http');

describe('07/http/client.js (public: alternative GET path and expected body)', () => {
  let server;

  afterEach((done) => {
    if (server && server.listening) server.close(done);
    else done();
  });

  test('http client (public) requests /public and receives different body', (done) => {
    server = http.createServer((req, res) => {
      if (req.url === '/public') {
        res.writeHead(200, { 'Content-Type': 'text/plain' });
        res.end('this is a public test\n');
      } else {
        res.writeHead(404);
        res.end();
      }
    }).listen(23338, () => {
      http.get({ port: 23338, path: '/public' }, (res) => {
        let body = '';
        res.setEncoding('utf8');
        res.on('data', d => { body += d; });
        res.on('end', () => {
          expect(body).toContain('public test');
          done();
        });
      }).on('error', done);
    });
  });
});