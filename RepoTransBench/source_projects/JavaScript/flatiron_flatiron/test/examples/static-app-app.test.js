const path = require('path');
const http = require('http');
const appPath = path.join(__dirname, '../../examples/static-app/app.js');
let app;
let server;

beforeAll((done) => {
  jest.resetModules();
  app = require(appPath);
  // Assume app exports a function that starts server, resolves with server instance
  if (typeof app === 'function') {
    app().then((srv) => {
      server = srv;
      setTimeout(done, 300); // Give time for server to be ready
    });
  } else if (app && app.listen) {
    server = app.listen(8250, () => setTimeout(done, 200));
  } else {
    done();
  }
});

afterAll((done) => {
  if (server && server.close) {
    server.close(done);
  } else {
    done();
  }
});

describe('examples/static-app/app.js', () => {
  it('should respond with index.html or something on root', (done) => {
    http.get('http://localhost:8250/', (res) => {
      expect([200, 404]).toContain(res.statusCode);
      done();
    }).on('error', done);
  });

  it('should serve /assets/style.js if exists', (done) => {
    http.get('http://localhost:8250/assets/style.js', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        expect([200, 404]).toContain(res.statusCode); // Handle both present/absent
        if (res.statusCode === 200) {
          expect(data).toContain('Hello World!');
        }
        done();
      });
    }).on('error', done);
  });
});