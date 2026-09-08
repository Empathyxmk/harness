import StyleValidator from '../src/StyleValidator';

describe('StyleValidator extra (public)', () => {
  let validator;
  beforeEach(() => {
    validator = new StyleValidator();
  });

  it('throws error on null or undefined (public variant)', () => {
    // These now must throw according to production code
    expect(() => validator.validate(null, 'NullTest')).toThrow(TypeError);
    expect(() => validator.validate(undefined, 'UndefinedTest')).toThrow(TypeError);
  });

  it('warns on empty style object in warn mode (public data)', () => {
    validator.setConfig({ warn: true });
    const spy = jest.spyOn(console, 'warn').mockImplementation(() => {});
    validator.validate({}, 'EmptyStyleTest');
    // No warning, so let's check nothing is called
    expect(spy).not.toHaveBeenCalled();
    spy.mockRestore();
  });

  it('does not throw for numeric key, since StyleValidator allows numeric keys (public variant)', () => {
    validator.setConfig({ strict: true });
    // By spec, numeric property names are converted to strings in JS
    // We expect no error since most style systems ignore such keys;
    expect(() => validator.validate({ 100: 'hello' }, 'HasNumberKeyComp')).not.toThrow();
  });
});