const fs = require('fs');
const https = require('https');
const path = require('path');

describe('07/https/server.js & client.js', () => {
  let server;
  const baseDir = path.join(__dirname, 'keys');
  const opts = {
    key: fs.readFileSync(path.join(baseDir, 'server.key')),
    cert: fs.readFileSync(path.join(baseDir, 'server.crt')),
    minVersion: 'TLSv1',
    ciphers: 'ALL:@SECLEVEL=0'
  };

  afterEach((done) => {
    if (server && server.listening) server.close(done);
    else done();
  });

  test('https server responds to https client', (done) => {
    server = https.createServer(opts, (req, res) => {
      res.writeHead(200);
      res.end('hello world\n');
    }).listen(18002, () => {
      const clientOpts = {
        hostname: 'localhost',
        port: 18002,
        path: '/',
        method: 'GET',
        key: fs.readFileSync(path.join(baseDir, 'client.key')),
        cert: fs.readFileSync(path.join(baseDir, 'client.crt')),
        rejectUnauthorized: false,
        minVersion: 'TLSv1',
        ciphers: 'ALL:@SECLEVEL=0'
      };
      const logs = [];
      const origLog = console.log;
      console.log = (msg) => logs.push(msg);

      const req = https.request(clientOpts, (res) => {
        res.setEncoding('utf8');
        let resp = '';
        res.on('data', d => { resp += d; });
        res.on('end', () => {
          expect(resp).toContain('hello world');
          console.log = origLog;
          done();
        });
      });
      req.end();
      req.on('error', (e) => {
        logs.push(e);
        console.log = origLog;
        done(e);
      });
    });
  });
});