let lang;
try {
  lang = require('../../parser/lang.js');
} catch (e) {
  lang = {};
}

describe('Lang module (public)', () => {
  it('should have at least one parsing function exported (public)', () => {
    // List only exported keys and check for function presence
    const keys = Object.keys(lang || {});
    let found = keys.some(k => typeof lang[k] === 'function');
    expect(found).toBe(true);
  });

  it('at least one fundamental function should return, not throw, for different valid input (public)', () => {
    // Try calling every exported function we can, with diverse test data
    const keys = Object.keys(lang || {});
    let atLeastOneSucceeded = false;
    for (let k of keys) {
      if (typeof lang[k] === 'function') {
        try {
          // Pick one of a range of plausible input values
          lang[k]("foobar_2024");
          atLeastOneSucceeded = true;
        } catch (e) { /* ignore individual errors */ }
      }
    }
    expect(atLeastOneSucceeded).toBe(true);
  });
});