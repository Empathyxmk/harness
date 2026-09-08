'use strict';

var expect = require('chai').expect;

describe('integration/originRedirect (public)', function () {
    it('should properly handle redirects (different route)', function () {
        function redirect(route) { return route + '?r=public'; }
        expect(redirect('/foopage')).to.equal('/foopage?r=public');
    });
});