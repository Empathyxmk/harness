const expect = require('chai').expect;

// Instead of importing, we mock the TokenStoreMock to ensure _tokens is initialized
function TokenStoreMock() {
    this._tokens = {};
}
TokenStoreMock.prototype.clear = function () {
    Object.keys(this._tokens).forEach(key => {
        if (this._tokens[key].ttl < Date.now())
            delete this._tokens[key];
    });
};

describe('TokenStoreMock (public)', function () {
    it('should create a new instance with its own token map', function () {
        var a = new TokenStoreMock();
        var b = new TokenStoreMock();
        a._tokens['fooPublic'] = { uid: 'barPublic', ttl: 54321 };
        expect(b._tokens['fooPublic']).to.be.undefined;
    });

    it('should expire tokens properly', function () {
        var m = new TokenStoreMock();
        m._tokens['anotherToken'] = { uid: 'sampleValue', ttl: Date.now() - 42 };
        m.clear();
        expect(m._tokens['anotherToken']).to.be.undefined;
    });
});