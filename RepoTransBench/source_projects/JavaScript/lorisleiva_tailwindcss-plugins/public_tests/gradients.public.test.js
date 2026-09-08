const test = require('ava');
const gradients = require('../gradients');

// New helper for public test, same structure, different fields if needed
function makeContext(overrides = {}) {
    return {
        addUtilities: overrides.addUtilities || (() => {}),
        e: overrides.e || ((x) => x),
        theme: overrides.theme || (() => ({})),
        variants: overrides.variants || (() => []),
    };
}

test('should export a function (public)', t => {
    t.is(typeof gradients, 'function');
});

// Use different gradient stops and types/keys for public test
test('should not throw and call addUtilities with a different mock theme (public)', t => {
    let called = false;
    gradients(makeContext({
        addUtilities: () => { called = true; },
        theme: () => ({
            red: ['to left', '#f00', '#fff'],
            yellow: { type: 'conic', colors: ['#ff0', '#fa0', '#f90'] }
        })
    }));
    t.true(called);
});