import Dog from "../src/dog";

describe("DOG PUBLIC: When checking the breed property on Dog", () => {
  it("should not have a breed property by default", () => {
    const d = new Dog();
    expect(d.breed).toBeUndefined();
  });
  it("should return the name as 'Dog'", () => {
    const d = new Dog();
    expect(d.name).toMatch(/Dog/);
  });
});