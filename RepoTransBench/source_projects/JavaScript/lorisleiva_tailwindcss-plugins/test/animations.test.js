const test = require('ava');
const animations = require('../animations');

function makeContext(overrides = {}) {
    return {
        addUtilities: overrides.addUtilities || (() => {}),
        e: overrides.e || ((x) => x),
        theme: overrides.theme || (() => ({})),
        variants: overrides.variants || (() => []),
    };
}

test('should call addUtilities with correct utilities and variants', t => {
    let added;
    const context = makeContext({
        addUtilities: (u, v) => { added = {u, v}; },
        e: (x) => `escaped-${x}`,
        theme: () => ({ bounce: 'bounce 1s infinite' }),
        variants: () => ['responsive'],
    });
    animations(context);
    t.deepEqual(added.u, [
        { '.escaped-bounce': { animation: 'bounce 1s infinite' } },
    ]);
    t.deepEqual(added.v, ['responsive']);
});

test('should work with empty animations theme', t => {
    let called = false;
    const context = makeContext({
        addUtilities: (u, v) => {
            called = true;
            t.deepEqual(u, []);
            t.deepEqual(v, []);
        },
        theme: () => ({}),
        variants: () => [],
    });
    animations(context);
    t.true(called);
});