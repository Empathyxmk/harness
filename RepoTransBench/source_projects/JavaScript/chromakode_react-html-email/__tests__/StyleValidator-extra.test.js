import StyleValidator from '../src/StyleValidator';

jest.spyOn(console, 'warn').mockImplementation(() => {});

describe('StyleValidator', () => {
  let validator;
  const supportMatrixMock = {
    "background-color": {
      "gmail": true,
      "yahoo-mail": false,
      "apple-mail": "Partial support",
    }
  };

  beforeEach(() => {
    validator = new StyleValidator();
    // patching the imported supportMatrix with only the mock for safe test
    validator.constructor.prototype.__supportMatrixBackup = validator.constructor.prototype.__supportMatrixBackup || require('../src/supportMatrix.json');
    Object.assign(require('../src/supportMatrix.json'), supportMatrixMock);
  });

  afterEach(() => {
    // Restore patched supportMatrix if needed
    const backup = validator.constructor.prototype.__supportMatrixBackup;
    if (backup) {
      Object.keys(require('../src/supportMatrix.json')).forEach(k => {
        if (!backup[k]) delete require('../src/supportMatrix.json')[k];
      });
      Object.assign(require('../src/supportMatrix.json'), backup);
    }
  });

  it('returns error on unknown property with strict', () => {
    const strictValidator = new StyleValidator({ strict: true });
    expect(strictValidator.validate({ notRealProp: 1 }, 'MockComp'))
      .toBeInstanceOf(Error);
  });

  it('returns undefined on unknown property if not strict', () => {
    const laxValidator = new StyleValidator({ strict: false });
    expect(laxValidator.validate({ notRealProp: 1 }, 'MockComp')).toBeUndefined();
  });

  it('returns warning for partially supported properties', () => {
    const validatorWarn = new StyleValidator({ warn: true, platforms: ['apple-mail'] });
    validatorWarn.validate({ backgroundColor: "blue" }, 'CompTest');
    expect(console.warn).toHaveBeenCalledWith(expect.stringContaining('partial support'));
  });

  it('returns error if property unsupported in platforms with strict', () => {
    const validatorStrict = new StyleValidator({ platforms: ['yahoo-mail', 'gmail'], strict: true });
    const result = validatorStrict.validate({ backgroundColor: "blue" }, 'X');
    expect(result).toBeInstanceOf(Error);
    expect(result.message).toMatch(/unsupported in: yahoo-mail/);
  });

  it('returns undefined if property is supported', () => {
    const validatorSupported = new StyleValidator({ platforms: ['gmail'], strict: true });
    expect(validatorSupported.validate({ backgroundColor: "blue" }, 'Y')).toBeUndefined();
  });

  it('handles empty style', () => {
    expect(validator.validate({}, 'Comp')).toBeUndefined();
  });
});