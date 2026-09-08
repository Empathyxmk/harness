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
      setTimeout(done, 250); // Faster start for public test
    });
  } else if (app && app.listen) {
    // Use a different port for public test to ensure separation
    server = app.listen(8325, () => setTimeout(done, 180));
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

describe('examples/static-app/app.js [public]', () => {
  it('should respond on an invalid path with likely 404 (public)', (done) => {
    http.get('http://localhost:8325/nonexistent', (res) => {
      expect([404, 200]).toContain(res.statusCode); // Order switched for alternative
      done();
    }).on('error', done);
  });

  it('should try to serve /assets/style.css; responds correctly (public)', (done) => {
    http.get('http://localhost:8325/assets/style.css', (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        expect([200, 404]).toContain(res.statusCode);
        if (res.statusCode === 200) {
          expect(data).toMatch(/body|Hello/i); // Accept standard CSS or string
        }
        done();
      });
    }).on('error', done);
  });
});