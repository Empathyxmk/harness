describe('monitor index exports', () => {
  it('should export Cpu, Mem, Net, Disk, Proc', () => {
    const monitor = require('./index');
    expect(monitor).toHaveProperty('Cpu');
    expect(monitor).toHaveProperty('Mem');
    expect(monitor).toHaveProperty('Net');
    expect(monitor).toHaveProperty('Disk');
    expect(monitor).toHaveProperty('Proc');
    // Types should be functions (constructors)
    expect(typeof monitor.Cpu).toBe('function');
  });
});