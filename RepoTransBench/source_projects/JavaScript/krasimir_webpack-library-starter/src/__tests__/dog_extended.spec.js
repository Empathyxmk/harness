import Dog from '../dog.ts';

describe('Dog class additional tests', () => {
  it('should construct with correct name', () => {
    const dog = new Dog();
    expect(dog.name).toBe('Dog');
  });

  it('should have oneThird static getter returning 3', () => {
    // The code has: return 3.0 / 1.0;
    expect(Dog.oneThird).toBe(3);
  });

  it('should have an accessible _name property', () => {
    const dog = new Dog();
    // Direct state test
    expect(dog._name).toBe('Dog');
  });
});