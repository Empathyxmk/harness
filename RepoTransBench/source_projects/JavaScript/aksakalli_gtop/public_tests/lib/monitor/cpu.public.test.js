const Cpu = require('../../../lib/monitor/cpu');

describe('Cpu (public)', () => {
  it('should construct and update sparkline/line with public data (public)', () => {
    const sparkline = { setData: jest.fn(), screen: { render: jest.fn() }};
    const line = { setData: jest.fn(), screen: { render: jest.fn() }};
    const cpu = new Cpu(sparkline, line);

    cpu.updateData([
      { times: { user: 20000, nice: 2222, sys: 3333, idle: 696969, irq: 100 } },
      { times: { user: 15000, nice: 1200, sys: 1800, idle: 50505, irq: 80 } },
    ]);
    // Both sparkline and line setData called
    expect(sparkline.setData).toHaveBeenCalled();
    expect(line.setData).toHaveBeenCalled();
    expect(sparkline.screen.render).toHaveBeenCalled();
    expect(line.screen.render).toHaveBeenCalled();
  });

  it('should handle empty array (public)', () => {
    const sparkline = { setData: jest.fn(), screen: { render: jest.fn() }};
    const line = { setData: jest.fn(), screen: { render: jest.fn() }};
    const cpu = new Cpu(sparkline, line);
    cpu.updateData([]);
    expect(sparkline.setData).toHaveBeenCalled();
    expect(line.setData).toHaveBeenCalled();
  });
});