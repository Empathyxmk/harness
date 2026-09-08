const APIError = require('../lib/errors/apierror');
const { expect } = require('chai');

describe('APIError (public)', () => {
  it('should set name, message, code, and status for different data', () => {
    const err = new APIError('another error occurred', 999);
    expect(err).to.be.instanceof(Error);
    expect(err).to.have.property('name', 'APIError');
    expect(err).to.have.property('message', 'another error occurred');
    expect(err).to.have.property('code', 999);
    expect(err).to.have.property('status', 500);
    expect(err.stack).to.be.a('string');
  });

  it('should use undefined for both missing values (public)', () => {
    const err = new APIError(undefined, undefined);
    expect(err.message).to.equal(undefined);
    expect(err.code).to.equal(undefined);
  });
});