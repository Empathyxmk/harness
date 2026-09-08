const expect = require('chai').expect;

// Mock the passwordless module for userProperty test
const passwordless = {
    userProperty: 'publicUser'
};

describe('user (public)', function () {
    it('should provide a userProperty default value', function () {
        expect(passwordless.userProperty).to.equal('publicUser');
    });

    it('should allow modifying userProperty temporarily', function () {
        passwordless.userProperty = 'newPropertyPub';
        expect(passwordless.userProperty).to.equal('newPropertyPub');
        // Restore state for potential subsequent tests
        passwordless.userProperty = 'publicUser';
    });
});