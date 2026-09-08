const TrafficLight = require('../State');

describe('TrafficLight State Pattern', () => {
  let light;

  beforeEach(() => {
    light = new TrafficLight();
  });

  test('Initial state is Green', () => {
    expect(light.sign()).toBe('GO');
  });

  test('Cycles from Green to Red to Yellow and back to Green', () => {
    light.change();
    expect(light.sign()).toBe('STOP'); // Red
    light.change();
    expect(light.sign()).toBe('STEADY'); // Yellow
    light.change();
    expect(light.sign()).toBe('GO'); // Back to Green
  });

  test('Multiple full cycles work correctly', () => {
    for(let i = 0; i < 9; i++) {
      light.change();
    }
    expect(light.sign()).toBe('GO');
  });
});