const transformsPlugin = require('./index');

function makeMockApi() {
  return {
    addUtilities: jest.fn(),
    addComponents: jest.fn(),
    theme: jest.fn((type) => {
      const presets = {
        translate: { 0: '0', 1: '0.25rem' },
        scale: { 0: '0', 1: '1' },
        rotate: { 0: '0', 45: '45deg' },
        skew: { 0: '0', 12: '12deg' },
        transformOrigin: { center: 'center', top: 'top', left: 'left' }
      };
      return presets[type] || {};
    }),
    e: x => x,
    variants: jest.fn((utility) => ['responsive', 'hover'])
  };
}

describe('transformsPlugin', () => {
  it('should call addUtilities and addComponents when run', () => {
    const api = makeMockApi();
    transformsPlugin(api);
    expect(api.addUtilities).toHaveBeenCalled();
    expect(api.addComponents).toHaveBeenCalled();
  });

  it('should use default options when none are provided', () => {
    const api = makeMockApi();
    transformsPlugin(api);
    // Check that utilities were added with correct default keys
    expect(Object.keys(api.addUtilities.mock.calls[0][0])).toContain('.transform-none');
  });

  it('should respect custom config', () => {
    const api = makeMockApi();
    const config = { respectImportant: true };
    transformsPlugin(api, config);
    expect(api.addUtilities).toHaveBeenCalled();
  });

  it('should handle absence of theme/variants gracefully', () => {
    const api = {
      addUtilities: jest.fn(),
      addComponents: jest.fn(),
      variants: jest.fn(() => []),
      theme: jest.fn(() => ({})),
      e: x => x
    };
    expect(() => transformsPlugin(api)).not.toThrow();
  });
});