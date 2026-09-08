const test = require('ava');
const gradients = require('../gradients');

// Helper context with all fields, matching the plugin call signature:
function makeContext(overrides = {}) {
    return {
        addUtilities: overrides.addUtilities || (() => {}),
        e: overrides.e || ((x) => x),
        theme: overrides.theme || (() => ({})),
        variants: overrides.variants || (() => []),
    };
}

test('should export a function', t => {
    t.is(typeof gradients, 'function');
});

test('should not throw and call addUtilities with a mock theme', t => {
    let called = false;
    gradients(makeContext({
        addUtilities: () => { called = true; },
        theme: () => ({
            blue: ['to right', '#00f', '#0ff'],
            green: { type: 'radial', colors: ['#0f0', '#ff0'] }
        })
    }));
    t.true(called);
});