const { shouldExcludePath } = require('./should-exclude-path');

jest.mock("micromatch", () => ({
  isMatch: jest.fn(() => false),
}));

describe('shouldExcludePath', () => {
  it('returns false for empty path', () => {
    expect(shouldExcludePath('', new Set(), [])).toBe(false);
  });

  it('returns true if path is in pathsToIgnore', () => {
    expect(shouldExcludePath('foo', new Set(['foo']), [])).toBe(true);
  });

  it('returns true if micromatch matches glob', () => {
    require('micromatch').isMatch.mockReturnValueOnce(true);
    expect(shouldExcludePath('bar', new Set(), ['bar'])).toBe(true);
  });

  it('returns false if no match', () => {
    expect(shouldExcludePath('baz', new Set(['xxx']), ['no'])).toBe(false);
  });

  it('strips leading ./ in globs', () => {
    require('micromatch').isMatch.mockReturnValueOnce(true);
    expect(shouldExcludePath('./baz', new Set(), ['baz'])).toBe(true);
  });

  it('handles empty globs', () => {
    expect(shouldExcludePath('baz', new Set(), [''])).toBe(false);
  });
});