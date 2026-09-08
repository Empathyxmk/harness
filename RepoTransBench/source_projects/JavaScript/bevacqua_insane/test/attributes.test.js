const attributes = require('../attributes');

describe('attributes', () => {
  it('should include known URI attributes', () => {
    expect(attributes.uris.href).toBe(true);
    expect(attributes.uris.src).toBe(true);
    expect(attributes.uris.background).toBe(true);
    expect(Object.keys(attributes.uris).length).toBeGreaterThan(4);
  });

  it('should not include non-URI attributes', () => {
    expect(attributes.uris.style).toBeUndefined();
  });
});