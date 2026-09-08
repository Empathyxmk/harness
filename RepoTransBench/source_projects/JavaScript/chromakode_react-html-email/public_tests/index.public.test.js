import * as mod from '../src/index';

describe('index exports (public)', () => {
  it('exports styleValidator instance', () => {
    expect(typeof mod.default.styleValidator).toBe('object');
    expect(mod.default.styleValidator.validate).toBeInstanceOf(Function);
  });

  it('exports configStyleValidator (public)', () => {
    expect(typeof mod.configStyleValidator).toBe('function');
  });

  it('exports PropTypes (public)', () => {
    // Should have property 'style' on PropTypes object
    expect(mod.PropTypes).toHaveProperty('style');
    expect(typeof mod.PropTypes.style).toBe('function');
  });
});