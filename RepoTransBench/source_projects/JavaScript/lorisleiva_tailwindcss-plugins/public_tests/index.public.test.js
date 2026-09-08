const test = require('ava');
const plugins = require('../index');

test('should export gradients plugin (public)', t => {
    t.truthy(plugins.gradients);
    t.is(typeof plugins.gradients, 'function');
});

// Confirm gradients plugin can be called (integration, public)
test('gradients plugin should accept a context and not throw (public)', t => {
    let called = false;
    plugins.gradients({
        addUtilities: () => { called = true; },
        e: (x) => x,
        theme: () => ({
            orange: ['to bottom', '#FFA500', '#FF6347']
        }),
        variants: () => []
    });
    t.true(called);
});