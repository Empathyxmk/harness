const { shouldExcludePath } = require('../src/should-exclude-path');

jest.mock("micromatch", () => ({
  isMatch: jest.fn(() => false),
}));

describe('shouldExcludePath (public)', () => {
  it('returns false for empty path (public)', () => {
    expect(shouldExcludePath('', new Set(), [])).toBe(false);
  });

  it('returns true if path is in pathsToIgnore (public)', () => {
    expect(shouldExcludePath('alpha', new Set(['alpha']), [])).toBe(true);
  });

  it('returns true if micromatch matches glob (public)', () => {
    require('micromatch').isMatch.mockReturnValueOnce(true);
    expect(shouldExcludePath('delta', new Set(), ['delta'])).toBe(true);
  });

  it('returns false if no match (public)', () => {
    expect(shouldExcludePath('epsilon', new Set(['zeta']), ['eta'])).toBe(false);
  });

  it('strips leading ./ in globs (public)', () => {
    require('micromatch').isMatch.mockReturnValueOnce(true);
    expect(shouldExcludePath('./theta', new Set(), ['theta'])).toBe(true);
  });

  it('handles empty globs (public)', () => {
    expect(shouldExcludePath('lambda', new Set(), [''])).toBe(false);
  });
});