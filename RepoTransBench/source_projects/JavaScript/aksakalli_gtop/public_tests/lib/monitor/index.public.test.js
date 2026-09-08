const Monitor = require('../../../lib/monitor/index');

describe('Monitor (public)', () => {
  it('should construct Monitor class (public)', () => {
    expect(() => {
      new Monitor();
    }).not.toThrow();
  });
});