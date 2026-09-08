const Net = require('./net');

describe('Net', () => {
  it('should construct with spark and update data', () => {
    const spark = { setData: jest.fn(), screen: { render: jest.fn() } };
    const net = new Net(spark);
    // updateData with fake net stats
    net.updateData([{
      iface: 'lo',
      rx_sec: 12345,
      tx_sec: 54321
    }]);
    expect(spark.setData).toHaveBeenCalled();
    expect(spark.screen.render).toHaveBeenCalled();
  });

  it('should handle no data gracefully', () => {
    const spark = { setData: jest.fn(), screen: { render: jest.fn() } };
    const net = new Net(spark);
    // empty data
    net.updateData([]);
    expect(spark.setData).toHaveBeenCalled();
    expect(spark.screen.render).toHaveBeenCalled();
  });
});