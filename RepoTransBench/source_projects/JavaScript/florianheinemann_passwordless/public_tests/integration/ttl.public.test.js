const expect = require('chai').expect;

describe('ttl integration (public)', function () {
    it('should expire tokens after a short ttl', function (done) {
        let tokenStore = {
            _tokens: { 'tok': { uid: 'uid', ttl: Date.now() + 10 } },
            clear: function () {
                Object.keys(this._tokens).forEach(key => {
                    if (this._tokens[key].ttl < Date.now()) delete this._tokens[key];
                });
            }
        };

        setTimeout(() => {
            tokenStore.clear();
            expect(tokenStore._tokens['tok']).to.be.undefined;
            done();
        }, 16); // Wait a little over the token's ttl
    });
});