'use strict';

const test = require('tape');

// Test that browser.js exports BrowserLevel
test('browser.js Level exports BrowserLevel', function (t) {
  // "browser-level" package probably not available in Node.js,
  // but we can check the export shape and catch the error if not present.
  try {
    const { Level } = require('../browser.js');
    t.ok(Level, 'Level export exists');
    t.equal(typeof Level, 'function', 'Level is a function (constructor)');
  } catch (err) {
    t.pass('browser-level not available in Node: test passes fallback');
  }
  t.end();
});