const Disk = require('../../lib/monitor/disk');

describe('Disk (public)', () => {
  it('should construct with donut and setInterval/clearInterval on update (public)', () => {
    const donut = { setData: jest.fn(), screen: { render: jest.fn() }};
    const disk = new Disk(donut);

    disk.updateData([{
      fs: '/dev/sdb2',
      size: 5000,
      used: 1234,
      use: 25,
      mount: '/mnt'
    }]);
    expect(Array.isArray(donut.setData.mock.calls[0][0])).toBe(true);
    expect(donut.setData).toHaveBeenCalled();
    expect(donut.screen.render).toHaveBeenCalled();
  });

  it('should handle no data gracefully (public)', () => {
    const donut = { setData: jest.fn(), screen: { render: jest.fn() }};
    const disk = new Disk(donut);
    // Provide a "disk" with null values to hit similar code path
    disk.updateData([{
      fs: null,
      size: null,
      used: null,
      use: null,
      mount: null
    }]);
    expect(donut.setData).toHaveBeenCalled();
    expect(donut.screen.render).toHaveBeenCalled();
  });
});