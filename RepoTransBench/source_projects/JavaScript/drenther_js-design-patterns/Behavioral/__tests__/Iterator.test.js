const { IteratorClass, iteratorUsingGenerator } = require('../Iterator');

describe('Iterator Pattern - IteratorClass', () => {
  test('Iterates over array elements correctly', () => {
    const data = [1,2,3];
    const iterator = new IteratorClass(data);
    const result = [];
    for (const item of iterator) {
      result.push(item);
    }
    expect(result).toEqual(data);
  });

  test('Iterates again after finishing (reset)', () => {
    const data = ['a', 'b'];
    const iterator = new IteratorClass(data);
    const result1 = [];
    for (const item of iterator) { result1.push(item); }
    const result2 = [];
    for (const item of iterator) { result2.push(item); }
    expect(result1).toEqual(data);
    expect(result2).toEqual(data);
  });
});

describe('Iterator Pattern - iteratorUsingGenerator', () => {
  test('Generator yields all items in order', () => {
    const data = [5,6,7];
    const gen = iteratorUsingGenerator(data);
    expect(Array.from(gen)).toEqual(data);
  });

  test('Generator on empty array yields nothing', () => {
    const data = [];
    const gen = iteratorUsingGenerator(data);
    expect(Array.from(gen)).toEqual([]);
  });
});