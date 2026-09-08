'use strict';

var expect = require('chai').expect;

describe('integration/standard (public)', function () {
    it('should do a basic equality check', function () {
        var a = 'foo';
        var b = 'foo';
        expect(a).to.equal(b);
    });
});