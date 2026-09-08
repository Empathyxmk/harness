const expect = require('chai').expect;
const pint = require('../lib/pint');

describe('pint', function () {
  it('should export an object with a "drink" function', function () {
    expect(pint).to.be.an('object');
    expect(pint).to.have.property('drink').that.is.a('function');
  });

  it('should return undefined when calling "drink"', () => {
    // drink() expects a jobQueue, let's pass a dummy or minimal object
    expect(() => pint.drink({})).to.not.throw();
    expect(pint.drink({})).to.be.undefined;
  });
});