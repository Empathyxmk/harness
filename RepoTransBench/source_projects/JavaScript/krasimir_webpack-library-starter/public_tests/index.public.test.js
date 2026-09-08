import * as bundle from "../src/index";
import Cat from "../src/cat";
import Dog from "../src/dog";

describe('INDEX PUBLIC: Bundle exports and custom property tests', () => {
  it('should have Cat and Dog exported as functions', () => {
    expect(typeof bundle.Cat).toBe("function");
    expect(typeof bundle.Dog).toBe("function");
  });

  it("should export Cat/and Dog distinct from built-ins and with correct names", () => {
    expect(bundle.Cat.name).toBe("Cat");
    expect(bundle.Dog.name).toBe("Dog");
    expect(bundle.Cat).not.toBe(Array);
    expect(bundle.Dog).not.toBe(Object);
  });

  it("Cat instance from bundle should match a Cat definition instance", () => {
    const bundleCat = new bundle.Cat();
    const localCat = new Cat();
    // Names should match
    expect(bundleCat.name).toBe(localCat.name);
    // Should be instance of both the imported Cat and bundle.Cat
    expect(bundleCat instanceof Cat).toBe(true);
    expect(bundleCat instanceof bundle.Cat).toBe(true);
  });

  it("Dog instance from bundle should match a Dog definition instance", () => {
    const bundleDog = new bundle.Dog();
    const localDog = new Dog();
    expect(bundleDog.name).toBe(localDog.name);
    expect(bundleDog instanceof Dog).toBe(true);
    expect(bundleDog instanceof bundle.Dog).toBe(true);
  });
});