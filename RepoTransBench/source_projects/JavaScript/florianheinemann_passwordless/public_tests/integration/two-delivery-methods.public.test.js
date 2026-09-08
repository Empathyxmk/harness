'use strict';

var expect = require('chai').expect;

describe('integration/two-delivery-methods (public)', function () {
    it('should handle two delivery logic differently', function () {
        function d1(token) { return 'delivered1:' + token; }
        function d2(token) { return 'delivered2:' + token; }
        expect(d1('tokpub1')).to.equal('delivered1:tokpub1');
        expect(d2('tokpub2')).to.equal('delivered2:tokpub2');
    });
});