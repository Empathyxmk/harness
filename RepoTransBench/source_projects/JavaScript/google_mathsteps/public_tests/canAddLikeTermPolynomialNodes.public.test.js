const canAddLikeTerms = require('../lib/checks/canAddLikeTerms');

const TestUtil = require('../test/TestUtil');

function testCanBeAdded(expr, addable) {
  TestUtil.testBooleanFunction(
    canAddLikeTerms.canAddLikeTermPolynomialNodes, expr, addable);
}

describe('can add like term polynomials (public)', () => {
  const tests = [
    ['y^4 + y^4', true],
    ['z + z', true],
    ['x^2 + y', false],
    ['a^3 + a', false],
    ['p^6 + p^6', true]
  ];
  tests.forEach(t => testCanBeAdded(t[0], t[1]));
});