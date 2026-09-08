const utils = require('../../lib/utils');

describe('utils.humanFileSize (public)', () => {
  it('should return "0.00 B" for 0 bytes (public)', () => {
    expect(utils.humanFileSize(0)).toBe('0.00 B');
  });

  it('should convert different bytes using binary units', () => {
    expect(utils.humanFileSize(4096)).toBe('4.00 KiB');
    expect(utils.humanFileSize(2097152)).toBe('2.00 MiB');
    // using a different small input for the double space
    expect(utils.humanFileSize(50)).toBe('50.00  B');
  });

  it('should convert bytes using decimal units with other values', () => {
    expect(utils.humanFileSize(2000, true)).toBe('2.00 KB');
    expect(utils.humanFileSize(2000000, true)).toBe('2.00 MB');
    expect(utils.humanFileSize(555, true)).toBe('555.00  B');
  });

  it('should append "i" for binary units except B (public)', () => {
    expect(utils.humanFileSize(8192)).toContain('KiB');
    expect(utils.humanFileSize(2097152)).toContain('MiB');
    // For bytes only e == 0, so no "i"
    expect(utils.humanFileSize(25)).toBe('25.00  B');
  });
});

describe('utils.colors (public)', () => {
  it('should have expected colors (public)', () => {
    expect(utils.colors).toEqual(['magenta', 'cyan', 'blue', 'yellow', 'green', 'red']);
    expect(utils.colors.length).toBe(6);
  });
});