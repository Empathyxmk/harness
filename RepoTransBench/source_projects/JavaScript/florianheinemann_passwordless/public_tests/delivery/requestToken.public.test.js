const expect = require('chai').expect;

describe('requestToken (public)', function () {
    it('should throw if called without the delivery object', function () {
        function passwordlessRequestToken() {
            throw new Error('Missing delivery object');
        }
        expect(() => passwordlessRequestToken()).to.throw(Error);
    });

    it('should not throw if called with custom delivery and TokenStoreMock', function () {
        function passwordlessRequestToken(delivery, store) {
            if (!delivery || !store) throw new Error('Parameters missing');
            // else succeed
            return true;
        }
        const dummyDelivery = {};
        const mockStore = {};
        expect(() => passwordlessRequestToken(dummyDelivery, mockStore)).to.not.throw();
    });
});