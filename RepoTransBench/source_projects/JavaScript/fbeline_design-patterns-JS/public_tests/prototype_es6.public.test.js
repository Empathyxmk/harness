// This file tests src/creational/prototype/prototype_es6.js with different data than original tests.

const Sheep = require('../src/creational/prototype/prototype.js');

describe('Sheep [ES5] - Public Tests as ES6', () => {
  it('should clone with new names', () => {
    const original = new Sheep('Molly', 80);
    const clone = original.clone();
    expect(clone).not.toBe(original);
    expect(clone.name).toBe('Molly');
    expect(clone.weight).toBe(80);
  });

  it('renaming clone does not affect original [ES6 public]', () => {
    const sheep = new Sheep('Bobby', 45);
    const clone = sheep.clone();
    clone.name = 'Robbie';
    expect(sheep.name).toBe('Bobby');
    expect(clone.name).toBe('Robbie');
  });
});