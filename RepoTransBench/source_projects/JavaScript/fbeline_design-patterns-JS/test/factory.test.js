const BmwFactory = require('../src/creational/factory/factory.js');

describe('BmwFactory', () => {
  test('returns X5 properties', () => {
    const car = BmwFactory('X5');
    expect(car.model).toBe('X5');
    expect(car.price).toBe(108000);
    expect(car.maxSpeed).toBe(300);
  });

  test('returns X6 properties', () => {
    const car = BmwFactory('X6');
    expect(car.model).toBe('X6');
    expect(car.price).toBe(111000);
    expect(car.maxSpeed).toBe(320);
  });

  test('returns undefined for unknown type', () => {
    expect(BmwFactory('X7')).toBeUndefined();
  });
});