const test = require('ava');

// Just check that module loads and exports something; deeper checks are in the plugin
const animations = require('../animations');

test('should export something from animations (public)', t => {
    t.truthy(animations);
    t.is(typeof animations, 'function');
});