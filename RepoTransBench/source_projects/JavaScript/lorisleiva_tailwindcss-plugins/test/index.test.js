const test = require('ava');
const plugins = require('../index');

test('should export gradients key', t => {
    t.truthy(plugins.gradients);
});