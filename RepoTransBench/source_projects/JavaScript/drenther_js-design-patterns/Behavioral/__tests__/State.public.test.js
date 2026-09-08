// PUBLIC TESTS - different data for State Pattern (TrafficLight)

const TrafficLight = require('../State');

describe('State Pattern (TrafficLight) - Public Tests', () => {
  test('Initial state sign is GO, after one change is STOP', () => {
    const light = new TrafficLight();
    expect(light.sign()).toBe('GO');
    light.change();
    expect(light.sign()).toBe('STOP');
  });

  test('After three changes cycles back to GO (cycle test)', () => {
    const light = new TrafficLight();
    light.change(); // STOP
    light.change(); // STEADY
    light.change(); // GO
    expect(light.sign()).toBe('GO');
  });

  test('Full cycle through states with explicit check', () => {
    const light = new TrafficLight();
    expect(light.sign()).toBe('GO'); // Green
    light.change();
    expect(light.sign()).toBe('STOP'); // Red
    light.change();
    expect(light.sign()).toBe('STEADY'); // Yellow
    light.change();
    expect(light.sign()).toBe('GO'); // Green again
  });
}
);