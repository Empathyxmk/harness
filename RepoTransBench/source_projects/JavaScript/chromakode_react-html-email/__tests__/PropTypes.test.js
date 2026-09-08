import React from 'react';
import PropTypesModule, { configStyleValidator } from '../src/PropTypes';

describe('PropTypes.style custom validator', () => {
  // We'll use React and checkPropTypes as intended!
  let styleProp = PropTypesModule.style;

  beforeEach(() => {
    configStyleValidator({ strict: true, warn: false });
  });

  function checkType(props) {
    // This matches what prop-types expects for custom validators
    // so we can safely use checkPropTypes
    const checkPropTypes = require('prop-types').checkPropTypes;
    // messages will appear on console.error so let's spy for them
    const spy = jest.spyOn(global.console, 'error').mockImplementation(() => {});
    // TypeSpec is matching key 'style' with our validator
    checkPropTypes({ style: styleProp }, props, 'style', 'TestComponent');
    spy.mockRestore();
    return spy;
  }

  it('does not error for null/undefined style', () => {
    const spy = checkType({});
    expect(spy).not.toHaveBeenCalled();
    const spy2 = checkType({ style: null });
    expect(spy2).not.toHaveBeenCalled();
  });

  it('errors for non-object style', () => {
    const spy = checkType({ style: "notanobject" });
    expect(spy).toHaveBeenCalled();
  });

  it('errors for unknown style property with strict', () => {
    configStyleValidator({ strict: true, warn: false, platforms: ["gmail"] });
    const spy = checkType({ style: { NotARealProperty: 13 } });
    expect(spy).toHaveBeenCalled();
  });

  it('does not error for valid style', () => {
    configStyleValidator({ strict: false, warn: false });
    // Should be safe and supported property (likely mapped in supportMatrix)
    const spy = checkType({ style: { backgroundColor: "red" } });
    expect(spy).not.toHaveBeenCalled();
  });
});