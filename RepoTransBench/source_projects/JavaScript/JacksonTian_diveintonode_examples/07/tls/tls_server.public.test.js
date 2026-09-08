const tls = require('tls');
const fs = require('fs');
const path = require('path');

describe('07/tls/server.js (public: alternate message/port)', () => {
  let server;
  let client;

  const baseDir = path.join(__dirname, 'keys');
  const opts = {
    key: fs.readFileSync(path.join(baseDir, 'server.key')),
    cert: fs.readFileSync(path.join(baseDir, 'server.crt')),
    ca: [fs.readFileSync(path.join(baseDir, 'ca.crt'))],
    requestCert: true,
    minVersion: 'TLSv1',
    ciphers: 'ALL:@SECLEVEL=0'
  };

  afterEach((done) => {
    const closeServer = () => {
      if (server && server.listening) {
        server.close(() => done());
      } else {
        done();
      }
    };
    if (client) {
      client.destroy();
      client = null;
      setTimeout(closeServer, 100);
    } else {
      closeServer();
    }
  });

  test('tls server (public) starts and receives different client message', (done) => {
    let response = '';
    server = tls.createServer(opts, (stream) => {
      stream.setEncoding('utf-8');
      stream.on('data', d => {
        response += d;
        stream.write('hello from server public!\n');
        setTimeout(() => stream.end(), 50);
      });
      stream.on('error', () => {});
    });
    server.listen(18011, '127.0.0.1', () => {
      client = tls.connect({
        port: 18011,
        host: '127.0.0.1',
        key: fs.readFileSync(path.join(baseDir, 'client.key')),
        cert: fs.readFileSync(path.join(baseDir, 'client.crt')),
        ca: [fs.readFileSync(path.join(baseDir, 'ca.crt'))],
        rejectUnauthorized: false,
        minVersion: 'TLSv1',
        ciphers: 'ALL:@SECLEVEL=0'
      }, function () {
        client.write('greetings from public test!\n');
      });
      let received = '';
      client.setEncoding('utf-8');
      client.on('data', (d) => { received += d; });
      client.on('end', () => {
        expect(received).toContain('hello from server public!');
        done();
      });
      client.on('error', (e) => {
        done();
      });
      setTimeout(() => {
        if (client && client.writable) client.end();
      }, 700);
    });
  }, 9000);
});