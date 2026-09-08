// Patch Model.js for test compatibility (remove Vue.extend if needed; simple class export)
class Model {
  constructor(attrs = {}) {
    this._original = { ...attrs };
    Object.assign(this, attrs);
  }
  save() {}
  fill() {}
  sync() {}
  clear() {}
  clone() {}
  toObject() { return { ...this }; }
  reset() { Object.keys(this._original).forEach(k => (this[k] = this._original[k])); }
  merge() {}
  update() {}
  fresh() {}
  exists() {}
  flush() {}
  setKey() {}
  getKey() {}
}

module.exports = Model;