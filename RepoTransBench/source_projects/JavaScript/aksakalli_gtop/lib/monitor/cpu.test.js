const Cpu = require('./cpu');
const utils = require('../utils');

jest.mock('systeminformation', () => ({
  currentLoad: jest.fn(),
}));

const si = require('systeminformation');

describe('Cpu', () => {
  let fakeLine, callbacks = [];
  beforeEach(() => {
    fakeLine = {
      setData: jest.fn(),
      screen: { render: jest.fn() }
    };
    callbacks = [];
    si.currentLoad.mockImplementation(cb => callbacks.push(cb));
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
    jest.clearAllMocks();
  });

  it('should initialize cpuData and set up an interval to update data', () => {
    const fakeData = {cpus: [
      { load: 10.123 },
      { load: 50.1 }
    ]};
    const cpuInstance = new Cpu(fakeLine);
    expect(callbacks.length).toBe(1);

    // Simulate systeminformation.currentLoad callback
    callbacks[0](fakeData);

    expect(cpuInstance.cpuData.length).toBe(2);
    expect(cpuInstance.cpuData[0].title).toContain('CPU1');
    expect(Array.isArray(cpuInstance.cpuData[0].y)).toBe(true);

    const newData = {cpus: [
      { load: 77.77 },
      { load: 22.4 }
    ]};
    // Simulate the interval call and its callback
    jest.advanceTimersByTime(1000);
    expect(callbacks.length).toBe(2);
    callbacks[1](newData);

    expect(fakeLine.setData).toHaveBeenCalled();
    expect(fakeLine.screen.render).toHaveBeenCalled();

    // Simulate updateData directly for coverage
    cpuInstance.updateData(newData);
    expect(cpuInstance.cpuData[0].title).toContain('%');
    expect(cpuInstance.cpuData[1].title).toContain('%');
  });
});