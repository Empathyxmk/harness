const APIError = require('../lib/errors/apierror');
const { expect } = require('chai');

describe('APIError', () => {
  it('should set name, message, code, and status', () => {
    const err = new APIError('something went wrong', 123);
    expect(err).to.be.instanceof(Error);
    expect(err).to.have.property('name', 'APIError');
    expect(err).to.have.property('message', 'something went wrong');
    expect(err).to.have.property('code', 123);
    expect(err).to.have.property('status', 500);
    expect(err.stack).to.be.a('string');
  });

  it('should use undefined for missing message or code', () => {
    const err = new APIError();
    expect(err.message).to.equal(undefined);
    expect(err.code).to.equal(undefined);
  });
});