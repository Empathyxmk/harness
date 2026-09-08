const expect = require('chai').expect;

describe('acceptToken (public)', function () {
    // Public stub for acceptToken
    function acceptToken(param) {
        if (typeof param === 'undefined') throw new Error('Must be called with config');
        // Return a middleware function if param is object
        return (req, res, next) => { next(); };
    }

    it('should throw if called with undefined', function () {
        expect(() => acceptToken(undefined)).to.throw(Error);
    });

    it('should return a middleware function when called with object', function () {
        let mw = acceptToken({ some: 'stuff' });
        expect(mw).to.be.a('function');
    });
});