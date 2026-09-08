const expect = require('chai').expect;

describe('acceptToken (public/session)', function () {
    // Public stub for Passwordless and express app simulation
    function PasswordlessMock() {
        this._tokens = {};
    }
    PasswordlessMock.prototype.validate = function(token, uid) {
        const entry = this._tokens[token];
        if (entry && entry.uid === uid && entry.ttl > Date.now()) return true;
        return false;
    };

    it('should authenticate successfully with a valid token and uid (diff values)', function () {
        var passwordless = new PasswordlessMock();
        var token = 'publicsessiontoken19';
        var uid = 'anotherTestUser';

        passwordless._tokens[token] = { uid: uid, ttl: Date.now() + 5000 };

        const out = passwordless.validate(token, uid);
        expect(out).to.be.true;
    });

    it('should return unauthorized for expired token', function () {
        var passwordless = new PasswordlessMock();
        var token = 'expiredpublictoken123';
        var uid = 'expiredUser';

        passwordless._tokens[token] = { uid: uid, ttl: Date.now() - 123 };
        const out = passwordless.validate(token, uid);
        expect(out).to.be.false;
    });
});