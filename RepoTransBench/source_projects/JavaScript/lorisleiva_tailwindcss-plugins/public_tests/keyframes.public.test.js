const test = require('ava');
const keyframes = require('../keyframes');
const shake = require('../keyframes/shake');

function makeContext(overrides = {}) {
    return {
        addUtilities: overrides.addUtilities || (() => {}),
        e: overrides.e || ((x) => x),
        theme: overrides.theme || (() => ({})),
    };
}

// Use a new keyframe name and opacity values
test('should call addUtilities with different keyframes (public)', t => {
    let added;
    const context = makeContext({
        addUtilities: (u) => { added = u; },
        e: (x) => `escaped2-${x}`,
        theme: () => ({
            bounce: { '0%': { opacity: .5 }, '100%': { opacity: .7 }},
        }),
    });
    keyframes(context);
    t.deepEqual(added, [
        { '@keyframes escaped2-bounce': { '0%': { opacity: .5 }, '100%': { opacity: .7 } } },
    ]);
});

test('should work with empty keyframes theme (public)', t => {
    let called = false;
    const context = makeContext({
        addUtilities: (u) => { called = true; t.deepEqual(u, []); },
        theme: () => ({}),
    });
    keyframes(context);
    t.true(called);
});

// shake.js: provide a different expectation on style (different property than original test)
test('shake.js: should add shake keyframes (public)', t => {
    let called = false;
    shake({
        addUtilities: (result) => {
            called = true;
            t.truthy(result['@keyframes shake']);
            // Instead of checking ['8%, 41%'], check for another property
            t.is(result['@keyframes shake']['100%']['transform'], 'translateX(0)');
        }
    });
    t.true(called);
});