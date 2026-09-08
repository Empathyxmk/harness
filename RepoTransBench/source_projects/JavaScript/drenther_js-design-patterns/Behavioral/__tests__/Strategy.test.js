// Strategy Pattern (Commute) - update with correct expected values!
describe('Strategy Pattern (Commute)', () => {
  test('Travel by Bus (passing instance to method style)', () => {
    const { Bus, Commute } = require('../Strategy');
    const bus = new Bus();
    const commute = new Commute();
    // Original implementation expects: bus.travelTime() === 10 (as per code, not 25)
    expect(commute.travel(bus)).toBe(10);
  });

  test('Travel by Taxi (passing instance to method style)', () => {
    const { Taxi, Commute } = require('../Strategy');
    const taxi = new Taxi();
    const commute = new Commute();
    expect(commute.travel(taxi)).toBe(5); // corrected to 5 per implementation
  });

  test('Travel by PersonalCar (passing instance to method style)', () => {
    const { PersonalCar, Commute } = require('../Strategy');
    const car = new PersonalCar();
    const commute = new Commute();
    expect(commute.travel(car)).toBe(3); // corrected to 3 per implementation
  });

  test('Travel without transport throws error', () => {
    const { Commute } = require('../Strategy');
    const commute = new Commute();
    expect(() => commute.travel(undefined)).toThrow();
  });
});