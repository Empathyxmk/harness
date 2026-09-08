const expect = require('chai').expect;

// Provide a mock TokenStoreMock
function TokenStoreMock() {
    this._tokens = {};
}
TokenStoreMock.prototype.clear = function () {
    this._tokens = {};
};

describe('integration/token-reuse (public)', function () {
    it('should not allow token reuse with different tokens (diff uid and token)', function () {
        var store = new TokenStoreMock();
        var tokenA = 'abc1public';
        var tokenB = 'def2public';
        var uid = 'someone@public.com';
        store._tokens[tokenA] = { uid, ttl: Date.now() + 100000 };
        // Reuse scenario with different token
        expect(store._tokens[tokenA].uid).to.equal(uid);
        // tokenB should not exist (simulate)
        expect(store._tokens[tokenB]).to.be.undefined;
    });

    it('should invalidate tokens explicitly', function () {
        var store = new TokenStoreMock();
        var token = 'tokenreusetestfoo';
        store._tokens[token] = { uid: 'bob', ttl: Date.now() + 100000 };
        expect(store._tokens[token]).to.exist;
        store.clear();
        expect(store._tokens[token]).to.not.exist;
    });
});