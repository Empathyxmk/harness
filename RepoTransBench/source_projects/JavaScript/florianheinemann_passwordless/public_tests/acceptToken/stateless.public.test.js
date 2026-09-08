const expect = require('chai').expect;

describe('acceptToken (public/stateless)', function () {
    // Public stub for Passwordless stateless checking
    function TokenStore() {
        this._tokens = {};
    }
    TokenStore.prototype.validate = function(token, uid) {
        const entry = this._tokens[token];
        if (entry && entry.uid === uid && entry.ttl > Date.now()) return true;
        return false;
    };

    it('should fail authentication with a random token', function () {
        var store = new TokenStore();
        // random token/uid never added
        expect(store.validate('foo', 'bar')).to.be.false;
    });

    it('should accept the right token (different random/uid)', function () {
        var store = new TokenStore();
        var token = 'tokensecure123';
        var uid = 'testuser42';

        store._tokens[token] = { uid: uid, ttl: Date.now() + 10000 };

        expect(store.validate(token, uid)).to.be.true;
    });
});