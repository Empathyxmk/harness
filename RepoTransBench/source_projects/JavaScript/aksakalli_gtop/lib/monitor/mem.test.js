const Mem = require('./mem');

describe('Mem', () => {
  let line, memDonut, swapDonut, mem;
  beforeEach(() => {
    line = {setData: jest.fn(), screen: {render: jest.fn()}};
    memDonut = {setData: jest.fn()};
    swapDonut = {setData: jest.fn()};
    mem = new Mem(line, memDonut, swapDonut);
  });

  it('should construct with line, memDonut, swapDonut and update data', () => {
    mem.memData = [
      { x: Array(20).fill(0), y: Array(20).fill(0), title: 'Memory %', style: {line: 'green'} },
      { x: Array(20).fill(0), y: Array(20).fill(0), title: 'Swap %', style: {line: 'yellow'} }
    ];
    mem.updateData({
      total: 1000,
      used: 600,
      swapused: 100,
      swaptotal: 200
    });

    expect(line.setData).toHaveBeenCalled();
    expect(line.screen.render).toHaveBeenCalled();
    expect(memDonut.setData).toHaveBeenCalled();
    expect(swapDonut.setData).toHaveBeenCalled();
  });

  it('should handle missing swap and memory data', () => {
    mem.memData = [
      { x: Array(20).fill(0), y: Array(20).fill(0), title: 'Memory %', style: {line: 'green'} },
      { x: Array(20).fill(0), y: Array(20).fill(0), title: 'Swap %', style: {line: 'yellow'} }
    ];
    mem.updateData({});

    expect(line.setData).toHaveBeenCalled();
    expect(memDonut.setData).toHaveBeenCalled();
    expect(swapDonut.setData).toHaveBeenCalled();
  });
});