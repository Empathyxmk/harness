const Disk = require('./disk');

describe('Disk', () => {
  it('should construct with donut and setInterval/clearInterval on update', () => {
    const donut = { setData: jest.fn(), screen: { render: jest.fn() }};
    const disk = new Disk(donut);

    disk.updateData([{
      fs: '/dev/sda1',
      size: 1000,
      used: 700,
      use: 70,
      mount: '/'
    }]);
    expect(Array.isArray(donut.setData.mock.calls[0][0])).toBe(true);
    expect(donut.setData).toHaveBeenCalled();
    expect(donut.screen.render).toHaveBeenCalled();
  });

  it('should handle no data gracefully', () => {
    const donut = { setData: jest.fn(), screen: { render: jest.fn() }};
    const disk = new Disk(donut);
    // Provide a "disk" with defined properties but undefined fields to hit code path
    disk.updateData([{
      fs: undefined,
      size: undefined,
      used: undefined,
      use: undefined,
      mount: undefined
    }]);
    expect(donut.setData).toHaveBeenCalled();
    expect(donut.screen.render).toHaveBeenCalled();
  });
});