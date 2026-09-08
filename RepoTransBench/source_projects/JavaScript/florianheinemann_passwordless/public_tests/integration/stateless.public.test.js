'use strict';

var expect = require('chai').expect;

describe('integration/stateless (public)', function () {
    it('should simulate stateless request/response', function () {
        function mockMiddleware(req, res, next) { req.touched = true; next(); }
        var req = {};
        mockMiddleware(req, {}, function() {});
        expect(req.touched).to.be.true;
    });
});