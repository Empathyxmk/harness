const Step = require('../../parser/Step');

describe('Step class/module (public)', () => {
  it('should be constructor or object (public)', () => {
    expect(['function', 'object']).toContain(typeof Step);
  });

  it('should create a step with a different step name (public)', () => {
    if (typeof Step === 'function') {
      const step = new Step('begin', 123);
      expect(step.name).toBe('begin');
      expect(step.value).toBe(123);
    }
  });
});