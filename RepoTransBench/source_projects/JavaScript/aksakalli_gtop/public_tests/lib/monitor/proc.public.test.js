const Proc = require('../../../lib/monitor/proc');

describe('Proc (public)', () => {
  it('should construct and update table with different values (public)', () => {
    const table = { setData: jest.fn(), screen: { render: jest.fn() }};
    const proc = new Proc(table);

    proc.updateData([
      {
        pid: 4322,
        user: 'bob',
        pr: '19',
        ni: '0',
        virt: 102400,
        res: 50200,
        shr: 23000,
        s: 'S',
        cpu: 3.4,
        mem: 1.6,
        time: '00:06:45',
        command: 'postgres'
      },
      {
        pid: 101,
        user: 'eve',
        pr: '20',
        ni: '0',
        virt: 15360,
        res: 8000,
        shr: 1000,
        s: 'S',
        cpu: 0.1,
        mem: 0.3,
        time: '00:00:18',
        command: 'cron'
      }
    ]);
    expect(table.setData).toHaveBeenCalled();
    expect(table.screen.render).toHaveBeenCalled();
  });

  it('should handle empty data array (public)', () => {
    const table = { setData: jest.fn(), screen: { render: jest.fn() }};
    const proc = new Proc(table);
    proc.updateData([]);
    expect(table.setData).toHaveBeenCalled();
    expect(table.screen.render).toHaveBeenCalled();
  });
});