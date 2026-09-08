// Simple Errors implementation for test compatibility
class Errors {
  constructor() {
    this.errors = {};
  }
  set(field, error) { this.errors[field] = error; }
  get(field) { return this.errors[field]; }
  has(field) { return this.errors.hasOwnProperty(field); }
  clear(field) { delete this.errors[field]; }
  push(field, error) {
    if (!Array.isArray(this.errors[field])) this.errors[field] = [];
    this.errors[field].push(error);
  }
  first(field) {
    const val = this.errors[field];
    return Array.isArray(val) ? val[0] : undefined;
  }
  merge(e) {
    for (const k of Object.keys(e.errors)) {
      if (!this.errors[k]) this.errors[k] = [];
      this.errors[k] = this.errors[k].concat(e.errors[k]);
    }
  }
  all() {
    return { ...this.errors };
  }
  toString() {
    return JSON.stringify(this.errors);
  }
}

module.exports = Errors;