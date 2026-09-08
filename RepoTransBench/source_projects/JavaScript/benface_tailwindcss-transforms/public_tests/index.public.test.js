const transformsPlugin = require('../index');

function makeCustomMockApi() {
  return {
    addUtilities: jest.fn(),
    addComponents: jest.fn(),
    theme: jest.fn((type) => {
      const customPresets = {
        translate: { 2: '0.5rem', 3: '0.75rem' },
        scale: { 2: '2', 3: '3' },
        rotate: { 90: '90deg', 180: '180deg' },
        skew: { 27: '27deg', 45: '45deg' },
        transformOrigin: { bottom: 'bottom', right: 'right', center: 'center' }
      };
      return customPresets[type] || {};
    }),
    e: x => `escape__${x}`,
    variants: jest.fn((utility) => ['focus', 'active'])
  };
}

describe('transformsPlugin (public)', () => {
  it('should call addUtilities and addComponents for different config', () => {
    const api = makeCustomMockApi();
    transformsPlugin(api);
    expect(api.addUtilities).toHaveBeenCalled();
    expect(api.addComponents).toHaveBeenCalled();
  });

  it('should use custom options and handle keys', () => {
    const api = makeCustomMockApi();
    transformsPlugin(api);
    // Check that utilities were added with correct custom keys
    const addedKeys = Object.keys(api.addUtilities.mock.calls[0][0]);
    expect(addedKeys).toContain('.transform-none');
    expect(addedKeys).toContain('.translate-x-2');
    expect(addedKeys).toContain('.translate-y-3');
  });

  it('should respect a new config option', () => {
    const api = makeCustomMockApi();
    const config = { crazyOption: false };
    transformsPlugin(api, config);
    expect(api.addUtilities).toHaveBeenCalled();
  });

  it('should handle absence of theme/variants gracefully on different mock', () => {
    const api = {
      addUtilities: jest.fn(),
      addComponents: jest.fn(),
      variants: jest.fn(() => []),
      theme: jest.fn(() => ({})),
      e: x => x,
    };
    expect(() => transformsPlugin(api)).not.toThrow();
  });
});