// PUBLIC TESTS - different data for Chain Of Responsibility CumulativeSum

const CumulativeSum = require('../ChainOfResponsibility');

describe('Chain Of Responsibility CumulativeSum - Public Tests', () => {
  test('Starting at 5, chain add 7, -4, 12', () => {
    const sum = new CumulativeSum(5);
    expect(sum.sum).toBe(5);
    sum.add(7);
    expect(sum.sum).toBe(12);
    sum.add(-4).add(12);
    expect(sum.sum).toBe(20);
  });

  test('Default initial value is 0, add multiples', () => {
    const sum = new CumulativeSum();
    expect(sum.sum).toBe(0);
    sum.add(10).add(-2).add(-8);
    expect(sum.sum).toBe(0); // [0+10=10, 10-2=8, 8-8=0]
  });

  test('Method chaining with different data', () => {
    const sum = new CumulativeSum();
    sum.add(2).add(3).add(6);
    expect(sum.sum).toBe(11);
  });
});