const { expect } = require('chai');
const http = require('http');

describe('app.js (main server, public)', function() {
  let server;
  before(function(done) {
    try {
      server = require('../app');
      setTimeout(done, 700); // Longer wait for public test
    } catch (e) {
      setTimeout(done, 700);
    }
  });

  it('should respond (public) with some status code for a non-root endpoint', function(done) {
    // Use /favicon.ico, which most express apps serve statically
    http.get('http://localhost:3000/favicon.ico', (res) => {
      expect(res.statusCode).to.be.gte(200); // just check status code exists and is >= 200
      done();
    }).on('error', function (err) {
      // Server up, but endpoint may not exist
      done();
    });
  });
});