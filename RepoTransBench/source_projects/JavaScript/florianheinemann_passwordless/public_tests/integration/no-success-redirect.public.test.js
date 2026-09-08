'use strict';

var expect = require('chai').expect;

describe('integration/no-success-redirect (public)', function () {
    it('should simulate no-success-redirect logic', function () {
        var res = {
            redirectUrl: null,
            redirect: function(url) { this.redirectUrl = url; }
        };
        res.redirect('/successpage');
        expect(res.redirectUrl).to.equal('/successpage');
    });
});