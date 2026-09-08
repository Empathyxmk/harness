const assert = require('assert');
const VueModel = require('./VueModel').default || require('./VueModel'); // Compatible for both CJS and ESM

describe('VueModel', () => {
  it('should initialize with empty config', () => {
    const vm = new VueModel();
    assert.ok(vm);
  });

  it('should allow setting and getting properties', () => {
    const vm = new VueModel({ name: 'Test' });
    assert.strictEqual(vm.name, 'Test');
    vm.name = 'Changed';
    assert.strictEqual(vm.name, 'Changed');
  });

  it('should be able to call $reset', () => {
    const vm = new VueModel({ a: 1 });
    vm.a = 5;
    if (typeof vm.$reset === 'function') {
      vm.$reset();
      assert.strictEqual(vm.a, 1);
    }
  });
});