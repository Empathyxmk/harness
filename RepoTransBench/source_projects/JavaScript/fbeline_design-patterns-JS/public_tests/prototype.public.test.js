const Sheep = require('../src/creational/prototype/prototype.js');

describe('Sheep [ES5] - Public Tests', () => {
  it('should clone with different data', () => {
    const original = new Sheep('Dolly', 60);
    const clone = original.clone();
    expect(clone).not.toBe(original);
    expect(clone.name).toBe('Dolly');
    expect(clone.weight).toBe(60);
  });

  it('should not mutate original after clone renamed (different data)', () => {
    const sheep = new Sheep('Larry', 53);
    const clone = sheep.clone();
    clone.name = 'Barry';
    expect(sheep.name).toBe('Larry');
    expect(clone.name).toBe('Barry');
  });
});