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

test('should call addUtilities with correct keyframes', t => {
    let added;
    const context = makeContext({
        addUtilities: (u) => { added = u; },
        e: (x) => `escaped-${x}`,
        theme: () => ({
            wiggle: { '0%': { opacity: 0 }, '100%': { opacity: 1 }},
        }),
    });
    keyframes(context);
    t.deepEqual(added, [
        { '@keyframes escaped-wiggle': { '0%': { opacity: 0 }, '100%': { opacity: 1 } } },
    ]);
});

test('should work with empty keyframes theme', t => {
    let called = false;
    const context = makeContext({
        addUtilities: (u) => { called = true; t.deepEqual(u, []); },
        theme: () => ({}),
    });
    keyframes(context);
    t.true(called);
});

// For shake.js (very little coverage previously)
test('shake.js: should add shake keyframes', t => {
    let called = false;
    shake({
        addUtilities: (result) => {
            called = true;
            t.truthy(result['@keyframes shake']);
            t.is(result['@keyframes shake']['8%, 41%']['transform'], 'translateX(-10px)');
        }
    });
    t.true(called);
});