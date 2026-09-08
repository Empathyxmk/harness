import PropTypes, { styleValidator, configStyleValidator } from '../src/PropTypes';
import checkPropTypes from 'prop-types/checkPropTypes';

describe('PropTypes (public)', () => {
  it('validates allowed style properties using checkPropTypes for public data', () => {
    const props = { style: { color: 'purple' } };
    const result = checkPropTypes(
      { style: PropTypes.style },
      props,
      'prop',
      'ColorCompPublic'
    );
    expect(result).toBeUndefined();
  });

  it('triggers warning on wrong type and message contains correct pattern (public)', () => {
    const props = { style: 1234 };
    const consoleErrorSpy = jest.spyOn(console, 'error').mockImplementation(() => {});
    checkPropTypes({ style: PropTypes.style }, props, 'prop', 'NotObjCompPublicAgain');
    // Instead of testing .toHaveBeenCalledWith, look for the expected substring in any call argument
    const errorCalledWith = consoleErrorSpy.mock.calls.some(
      call =>
        call[0] &&
        call[0].includes("Invalid prop `style`") &&
        call[0].includes("supplied to `NotObjCompPublicAgain`")
    );
    expect(errorCalledWith).toBe(true);
    consoleErrorSpy.mockRestore();
  });

  it('calls styleValidator.validate for style object (public)', () => {
    const spy = jest.spyOn(styleValidator, 'validate').mockImplementation();
    const props = { style: { background: '#fff' } };
    checkPropTypes({ style: PropTypes.style }, props, 'prop', 'BGCompPublicAgain');
    expect(spy).toHaveBeenCalledWith({ background: '#fff' }, 'BGCompPublicAgain');
    spy.mockRestore();
  });

  it('configStyleValidator modifies config (public)', () => {
    const spy = jest.spyOn(styleValidator, 'setConfig').mockImplementation();
    const config = { customWarn: true };
    configStyleValidator(config);
    expect(spy).toHaveBeenCalledWith(config);
    spy.mockRestore();
  });
});