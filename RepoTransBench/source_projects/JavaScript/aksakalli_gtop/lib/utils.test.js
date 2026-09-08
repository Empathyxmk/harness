const utils = require('./utils');

describe('utils.humanFileSize', () => {
  it('should return "0.00 B" for 0 bytes', () => {
    expect(utils.humanFileSize(0)).toBe('0.00 B');
  });

  it('should convert bytes using binary (default) units', () => {
    expect(utils.humanFileSize(1024)).toBe('1.00 KiB');
    expect(utils.humanFileSize(1048576)).toBe('1.00 MiB');
    // Note: actual output has double space before "B" for size < 1024, due to how string is composed
    expect(utils.humanFileSize(100)).toBe('100.00  B');
  });

  it('should convert bytes using decimal units when isDecimal is true', () => {
    expect(utils.humanFileSize(1000, true)).toBe('1.00 KB');
    expect(utils.humanFileSize(1000000, true)).toBe('1.00 MB');
    expect(utils.humanFileSize(999, true)).toBe('999.00  B');
  });

  it('should append "i" for binary units except B', () => {
    expect(utils.humanFileSize(2048)).toContain('KiB');
    expect(utils.humanFileSize(1048576)).toContain('MiB');
    // For bytes only e == 0, so no "i"
    expect(utils.humanFileSize(10)).toBe('10.00  B');
  });
});

describe('utils.colors', () => {
  it('should have expected colors', () => {
    expect(utils.colors).toEqual(['magenta', 'cyan', 'blue', 'yellow', 'green', 'red']);
    expect(utils.colors.length).toBe(6);
  });
});