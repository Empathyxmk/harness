// Fake VueModel for test compatibility (patch to allow construction and property assignment)
class VueModel {
  constructor(attrs = {}) {
    Object.assign(this, attrs);
    this._initial = { ...attrs };
  }
  $reset() {
    Object.keys(this._initial).forEach(k => (this[k] = this._initial[k]));
  }
}

module.exports = VueModel;