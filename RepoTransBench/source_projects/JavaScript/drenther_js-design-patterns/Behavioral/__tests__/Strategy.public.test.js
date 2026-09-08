// Strategy Pattern (Commute) - PUBLIC TESTS (different data)

describe('Strategy Pattern (Commute) - Public Tests', () => {
  test('Travel by Bus with custom method (simulate delay)', () => {
    const { Bus, Commute } = require('../Strategy');
    // We'll monkey-patch Bus to simulate a delay for this public data test
    class DelayedBus extends Bus {
      travelTime() { return 14; }
    }
    const bus = new DelayedBus();
    const commute = new Commute();
    expect(commute.travel(bus)).toBe(14);
  });

  test('Travel by Taxi (simulate surge pricing)', () => {
    const { Taxi, Commute } = require('../Strategy');
    // Simulate surge-pricing taxi
    class ExpensiveTaxi extends Taxi {
      travelTime() { return 8; }
    }
    const taxi = new ExpensiveTaxi();
    const commute = new Commute();
    expect(commute.travel(taxi)).toBe(8);
  });

  test('Travel by PersonalCar (heavy traffic situation)', () => {
    const { PersonalCar, Commute } = require('../Strategy');
    // Simulate heavy traffic with personal car
    class SlowCar extends PersonalCar {
      travelTime() { return 9; }
    }
    const car = new SlowCar();
    const commute = new Commute();
    expect(commute.travel(car)).toBe(9);
  });

  test('Travel with invalid transport (object with no travelTime method)', () => {
    const { Commute } = require('../Strategy');
    const commute = new Commute();
    // Pass an object without travelTime method
    expect(() => commute.travel({})).toThrow();
  });
});