const Mem = require('../../../lib/monitor/mem');

describe('Mem (public)', () => {
  it('should construct with donut and update with different values (public)', () => {
    const donut = { setData: jest.fn(), screen: { render: jest.fn() }};
    const mem = new Mem(donut);

    mem.updateData({
      total: 16384,
      used: 4096,
      free: 12288,
      swapTotal: 2048,
      swapUsed: 1024,
      swapFree: 1024,
    });
    expect(Array.isArray(donut.setData.mock.calls[0][0])).toBe(true);
    expect(donut.setData).toHaveBeenCalled();
    expect(donut.screen.render).toHaveBeenCalled();
  });

  it('should handle null data gracefully (public)', () => {
    const donut = { setData: jest.fn(), screen: { render: jest.fn() }};
    const mem = new Mem(donut);
    mem.updateData(null);
    expect(donut.setData).not.toHaveBeenCalled();
    expect(donut.screen.render).not.toHaveBeenCalled();
  });
});