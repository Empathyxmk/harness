const Net = require('../../../lib/monitor/net');

describe('Net (public)', () => {
  it('should construct and update table with different values (public)', () => {
    const table = { setData: jest.fn(), screen: { render: jest.fn() }};
    const net = new Net(table);

    net.updateData([
      {
        iface: 'eth2',
        rx_bytes: 1000888,
        tx_bytes: 9100,
        rx_errors: 1,
        tx_errors: 0
      },
      {
        iface: 'wlan1',
        rx_bytes: 8899,
        tx_bytes: 15663,
        rx_errors: 0,
        tx_errors: 0
      }
    ]);
    expect(table.setData).toHaveBeenCalled();
    expect(table.screen.render).toHaveBeenCalled();
  });

  it('should handle empty data array (public)', () => {
    const table = { setData: jest.fn(), screen: { render: jest.fn() }};
    const net = new Net(table);
    net.updateData([]);
    expect(table.setData).toHaveBeenCalled();
    expect(table.screen.render).toHaveBeenCalled();
  });
});