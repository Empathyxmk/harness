const canMultiplyLikeTermPolynomialNodes = require('../lib/checks/canMultiplyLikeTermPolynomialNodes');

const TestUtil = require('../test/TestUtil');

function testCanBeMultiplied(expr, multipliable) {
  TestUtil.testBooleanFunction(canMultiplyLikeTermPolynomialNodes, expr, multipliable);
}

describe('can multiply like term polynomials (public)', () => {
  const tests = [
    // test similar to x^2 * x^5 = true, but with different variables and powers
    ['y^3 * y^2', true],
    // x^3 * y^2 = false
    ['a^4 * b^2', false],
    // z^2 * z^2 = true
    ['z^2 * z^2', true]
  ];
  tests.forEach(t => testCanBeMultiplied(t[0], t[1]));
});