const canMultiplyLikeTermConstantNodes = require('../lib/checks/canMultiplyLikeTermConstantNodes');

const TestUtil = require('../test/TestUtil');

function testCanBeMultipliedConstants(expr, multipliable) {
  TestUtil.testBooleanFunction(canMultiplyLikeTermConstantNodes, expr, multipliable);
}

describe('can multiply like term constants (public)', () => {
  const tests = [
    ['4^2 * 4^3', true],
    ['5^2 * 6^2', false],
    ['7^3 * 7^1', true],
    ['2^5 * 2^2', true],
    ['9^1 * 8^1', false],
    ['12^2 * 12^4', true]
  ];
  tests.forEach(t => testCanBeMultipliedConstants(t[0], t[1]));
});