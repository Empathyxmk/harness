const assert = require('assert');
const VueModel = require('../src/VueModel');

// The following tests check constructed Model objects and registry

describe('VueModel (public)', () => {
  beforeEach(() => {
    VueModel.registry = {};
  });

  it('registers models with unique new data', () => {
    VueModel.register('widgets', { http: { baseRoute: '/widgets' } });
    assert.ok(VueModel.registry.widgets);
    assert.strictEqual(VueModel.registry.widgets.http.baseRoute, '/widgets');
  });

  it('registers multiple models with other names', () => {
    VueModel.register('things', { http: { baseRoute: '/things' } });
    VueModel.register('gadgets', { http: { baseRoute: '/gadgets' } });
    assert.ok(VueModel.registry.things);
    assert.ok(VueModel.registry.gadgets);
    assert.strictEqual(VueModel.registry.gadgets.http.baseRoute, '/gadgets');
  });
});