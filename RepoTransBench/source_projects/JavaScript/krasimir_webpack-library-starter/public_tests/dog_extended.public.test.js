import Dog from "../src/dog";

describe("DOG EXTENDED PUBLIC: Testing Dog with different input/output", () => {
  it("should always have name 'Dog' regardless of input", () => {
    // The implementation always sets this.name = 'Dog' regardless of arguments.
    const d = new Dog("Max");
    expect(d.name).toBe("Dog");
  });

  it("should not set color by default or when provided since color is not implemented", () => {
    const d = new Dog();
    expect(d.color).toBeUndefined();

    const coloredDog = new Dog("Rex", "white");
    expect(coloredDog.color).toBeUndefined();
  });
});