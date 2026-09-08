const Sheep = require('../src/creational/prototype/prototype.js');

describe('Sheep [ES5]', () => {
  it('should clone', () => {
    const original = new Sheep('Original', 75);
    const clone = original.clone();
    expect(clone).not.toBe(original);
    expect(clone.name).toBe('Original');
    expect(clone.weight).toBe(75);
  });

  it('should not mutate original after clone renamed', () => {
    const sheep = new Sheep('Henry', 40);
    const clone = sheep.clone();
    clone.name = 'Not Henry';
    expect(sheep.name).toBe('Henry');
    expect(clone.name).toBe('Not Henry');
  });
});