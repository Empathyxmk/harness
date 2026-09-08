const attributes = require('../attributes');

describe('attributes (public)', () => {
  it('should include other known URI attributes', () => {
    expect(attributes.uris.usemap).toBe(true);
    expect(attributes.uris.longdesc).toBe(true);
    expect(attributes.uris.base).toBe(true);
    expect(Object.keys(attributes.uris)).toEqual(
      expect.arrayContaining(['href', 'usemap', 'longdesc', 'src', 'cite', 'background', 'base'])
    );
  });

  it('should not include random attribute', () => {
    expect(attributes.uris.alt).toBeUndefined();
    expect(attributes.uris.class).toBeUndefined();
  });
});