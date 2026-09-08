const expect = require('chai').expect;

describe('addDelivery (public)', function () {
    it('should not throw if called with a valid delivery strategy', function () {
        function addDelivery(strategy) {
            if (!strategy || typeof strategy !== 'object' || typeof strategy.sendToken !== 'function') {
                throw new Error('Passwordless.addDelivery called with wrong parameters');
            }
        }
        const dummy = { sendToken: function () {} };
        expect(function() {
            addDelivery(dummy);
        }).not.to.throw();
    });
});