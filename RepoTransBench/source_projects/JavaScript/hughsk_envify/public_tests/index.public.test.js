jest.mock('../custom', () => jest.fn(() => 'PUBLIC_MOCK_CUSTOM'), { virtual: true });
const custom = require('../custom');
const envify = require('../index');

describe('index.js (public)', () => {
  it('exports result of custom(process.env) with different value', () => {
    expect(envify).toBe('PUBLIC_MOCK_CUSTOM');
    expect(custom).toHaveBeenCalledWith(process.env);
  });
});