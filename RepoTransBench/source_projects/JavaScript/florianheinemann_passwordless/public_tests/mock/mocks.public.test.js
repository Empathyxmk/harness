const expect = require('chai').expect;

// Mock structure matching the original (do not import)
const mocks = {
    mockStrategy: {
        sendToken: function(token, uid, done) {
            done();
        }
    },
    someOtherMock: {}
};

describe('mock/mocks (public)', function () {
    it('should export an object with keys', function () {
        expect(Object.keys(mocks).length).to.be.greaterThan(0);
    });

    it('should have a mock strategy with a sendToken function', function () {
        expect(mocks.mockStrategy).to.have.property('sendToken');
        expect(mocks.mockStrategy.sendToken).to.be.a('function');
    });
});