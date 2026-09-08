import Cat from '../cat.js';

describe('Cat class', () => {
  it('should construct with correct name', () => {
    const cat = new Cat();
    expect(cat.name).toBe('Cat');
  });

  it('should have an accessible _name property', () => {
    const cat = new Cat();
    // Directly testing internal state for completeness
    expect(cat._name).toBe('Cat');
  });
});