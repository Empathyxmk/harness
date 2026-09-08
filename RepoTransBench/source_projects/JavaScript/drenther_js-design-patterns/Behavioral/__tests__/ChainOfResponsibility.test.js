const CumulativeSum = require('../ChainOfResponsibility');

describe('Chain Of Responsibility CumulativeSum', () => {
  test('Initial value, add values and chain', () => {
    const sum = new CumulativeSum(2);
    expect(sum.sum).toBe(2);
    sum.add(3);
    expect(sum.sum).toBe(5);
    sum.add(-2).add(7);
    expect(sum.sum).toBe(10);
  });

  test('Default initial value is 0', () => {
    const sum = new CumulativeSum();
    expect(sum.sum).toBe(0);
  });

  test('Method chaining works', () => {
    const sum = new CumulativeSum();
    sum.add(1).add(4).add(5);
    expect(sum.sum).toBe(10);
  });
});