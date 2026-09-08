jest.mock('./custom', () => jest.fn(() => 'MOCKED_CUSTOM'), { virtual: true });
const custom = require('./custom');
const envify = require('./index');

describe('index.js', () => {
  it('exports result of custom(process.env)', () => {
    expect(envify).toBe('MOCKED_CUSTOM');
    expect(custom).toHaveBeenCalledWith(process.env);
  });
});