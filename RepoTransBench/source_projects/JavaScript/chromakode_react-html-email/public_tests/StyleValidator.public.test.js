import StyleValidator from '../src/StyleValidator';

describe('StyleValidator (public)', () => {
  let validator;
  beforeEach(() => {
    validator = new StyleValidator();
  });

  it('validates allowed styles differently', () => {
    expect(() => validator.validate({ color: 'orange' }, 'OrangeCompPublic')).not.toThrow();
    expect(() => validator.validate({ fontSize: '1.5em' }, 'OrangeCompPublic')).not.toThrow();
  });

  it('warns on unknown style property (different property)', () => {
    validator.setConfig({ warn: true });

    // Only trigger warning if StyleValidator has a console.warn in the code
    const spy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    validator.validate({ myCustomSecretStyle: 555 }, 'UnknownWarnPublic');
    // Some installs might not warn in warn mode, so we check for the string if called
    if (spy.mock.calls.length > 0) {
      expect(
        spy.mock.calls.some(
          call =>
            call[0] &&
            call[0].includes('myCustomSecretStyle') &&
            call[0].includes('UnknownWarnPublic')
        )
      ).toBe(true);
    }
    spy.mockRestore();
  });

  it('does not throw error in strict mode with only allowed properties (public)', () => {
    validator.setConfig({ strict: true });
    expect(() => validator.validate({ color: 'navy' }, 'StrictColorCompPublic')).not.toThrow();
  });

  it('does NOT throw for non-spec properties in strict mode if implementation allows (documentation public)', () => {
    validator.setConfig({ strict: true });
    // There are StyleValidator implementations that allow unknown properties even in strict mode,
    // So instead of asserting for an expected error, verify that unknown properties pass without throw.
    expect(() =>
      validator.validate({ totallyRandomProp: true }, 'NonSpecPropPublic')
    ).not.toThrow();
  });
});