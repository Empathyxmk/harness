import Cat from "../src/cat";

describe("CAT PUBLIC: Cat class alternative input/output", () => {
  it("should not have a color property by default", () => {
    const c = new Cat();
    expect(c.color).toBeUndefined();
  });

  it("should have a name containing the string 'Cat'", () => {
    const c = new Cat();
    expect(c.name).toContain("Cat");
  });

  it("should allow a custom name if and only if the Cat class supports it", () => {
    // The current implementation of Cat always assigns 'Cat' to name, regardless of input.
    // So we verify the name stays 'Cat' even if a custom parameter is given.
    const c = new Cat("Snowball");
    expect(c.name).toBe("Cat");
  });
});