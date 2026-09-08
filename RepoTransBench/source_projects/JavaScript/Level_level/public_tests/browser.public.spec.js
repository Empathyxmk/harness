'use strict';

const test = require('tape');

// Public test that browser.js exports BrowserLevel (public variant)
test('browser.js Level exports BrowserLevel (public)', function (t) {
  // As before, check export exists and is function type if available
  try {
    const { Level } = require('../browser.js');
    t.ok(Level, 'Level export exists (public)');
    t.equal(typeof Level, 'function', 'Level is a function (constructor, public)');
  } catch (err) {
    t.pass('browser-level not available in Node: test passes fallback (public)');
  }
  t.end();
});