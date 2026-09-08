const canRearrangeCoefficient = require('../lib/checks/canRearrangeCoefficient');

const TestUtil = require('../test/TestUtil');

function testCanBeRearranged(expr, arrangeable) {
  TestUtil.testBooleanFunction(canRearrangeCoefficient, expr, arrangeable);
}

describe('can rearrange coefficient (public)', () => {
  const tests = [
    ['a*5', true],
    ['z^2 * 4', true],
    ['m*1', true],
    ['b^4 * 11', true],
    ['q^7 * 10', true]
  ];
  tests.forEach(t => testCanBeRearranged(t[0], t[1]));
});