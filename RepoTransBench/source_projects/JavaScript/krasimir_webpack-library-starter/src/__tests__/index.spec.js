import bundle from '../index.js';
import Cat from '../cat.js';
import Dog from '../dog.ts';

describe('Index bundle', () => {
  it('should export Cat and Dog', () => {
    expect(bundle.Cat).toBe(Cat);
    expect(bundle.Dog).toBe(Dog);
  });

  it('should instantiate Cat and Dog via bundle', () => {
    const c = new bundle.Cat();
    const d = new bundle.Dog();
    expect(c.name).toBe('Cat');
    expect(d.name).toBe('Dog');
  });
});