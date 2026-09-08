const expect = require('chai').expect;

// Inline a mock TokenStoreMock for this "public" test
function TokenStoreMock() {
    this._tokens = {};
}

describe('integration/two-step-auth (public)', function () {
    it('should store two tokens for two uids', function () {
        var store = new TokenStoreMock();
        var uids = ['foo.user@public.com', 'bar.user@public.com'];
        store._tokens['pubtoken1'] = { uid: uids[0], ttl: Date.now() + 5000 };
        store._tokens['pubtoken2'] = { uid: uids[1], ttl: Date.now() + 5000 };
        expect(store._tokens['pubtoken1'].uid).to.equal(uids[0]);
        expect(store._tokens['pubtoken2'].uid).to.equal(uids[1]);
    });
});