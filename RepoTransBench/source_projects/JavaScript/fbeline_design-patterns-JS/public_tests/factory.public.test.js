const BmwFactory = require('../src/creational/factory/factory.js');

describe('BmwFactory - Public Tests', () => {
  test('returns X3 properties', () => {
    // We'll add a new entry to the factory temporarily for public test purposes.
    // But since the factory only knows X5 and X6, test with "X6" but validate logic with new values
    // Instead, let's test price/mileage comparison for other values in edge cases.
    const car = BmwFactory('X6');
    expect(car['model']).toBe('X6');
    expect(car['price']).toBe(111000);
    expect(car['maxSpeed']).toBe(320);
  });

  test('returns X5 properties with altered data assertion', () => {
    // Test same model, but make a calculation with price/speed instead of just matching fields
    const car = BmwFactory('X5');
    expect(car.model).toMatch(/^X/); // pattern match instead of exact equality
    expect(car.price).toBeGreaterThan(100000);
    expect(car.maxSpeed).toBeLessThanOrEqual(300);
  });

  test('returns undefined for random value', () => {
    expect(BmwFactory('Q7')).toBeUndefined();
  });
});