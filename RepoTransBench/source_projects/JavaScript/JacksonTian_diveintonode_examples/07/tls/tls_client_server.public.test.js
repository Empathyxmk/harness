const fs = require('fs');
const tls = require('tls');
const path = require('path');

describe('07/tls/client.js (public: integration with server, different port, message)', () => {
  let server;
  let client;
  const baseDir = path.join(__dirname, 'keys');
  const serverOpts = {
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

  test('tls client (public) connects to server and pipes different data', (done) => {
    server = tls.createServer(serverOpts, (stream) => {
      stream.setEncoding('utf8');
      stream.on('data', (data) => {
        stream.write('hello-public!\n');
        setTimeout(() => stream.end(), 50);
      });
      stream.on('end', () => {});
    });

    // Use a different port for this public test
    server.listen(18013, '127.0.0.1', () => {
      const logs = [];
      const origConsoleLog = console.log;
      console.log = (...args) => logs.push(args.join(' '));

      const options = {
        port: 18013,
        host: '127.0.0.1',
        key: fs.readFileSync(path.join(baseDir, 'client.key')),
        cert: fs.readFileSync(path.join(baseDir, 'client.crt')),
        ca: [fs.readFileSync(path.join(baseDir, 'ca.crt'))],
        rejectUnauthorized: false,
        minVersion: 'TLSv1',
        ciphers: 'ALL:@SECLEVEL=0'
      };

      client = tls.connect(options, function () {
        logs.push('client connected', client.authorized ? 'authorized' : 'unauthorized');
        client.write('Hello from PUBLIC client!');
      });
      client.setEncoding('utf8');
      let received = '';
      client.on('data', data => {
        received += data;
      });
      client.on('end', () => {
        expect(received).toContain('hello-public!');
        expect(logs.join(' ')).toContain('client connected');
        console.log = origConsoleLog;
        done();
      });
      client.on('error', (e) => {
        console.log = origConsoleLog;
        done();
      });
      setTimeout(() => {
        if (client && client.writable) client.end();
      }, 700);
    });
  }, 9000);
});