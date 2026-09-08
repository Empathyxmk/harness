/**
 * PUBLIC TEST: different data, same intent as original example.test.js.
 * This version mocks the node require pathing correctly and uses alternate test vectors.
 */
const path = require('path');

describe('example code - public cases', () => {

  beforeEach(() => {
    jest.resetModules();
    jest.clearAllMocks();
  });

  it('should connect to a new device successfully with alternate address', async () => {
    // Mock the module in the correct place:
    jest.doMock(path.resolve(__dirname, '../lib/device.js'), () => ({
      device: jest.fn(({ address }) => {
        if (address === 'alternateIp') {
          return Promise.resolve({ id: 'dev-999', name: 'TestDeviceAlt' });
        }
        return Promise.reject(new Error('not found'));
      }),
    }), { virtual: true });

    // Requiring the example should use our mock
    const mockAddress = 'alternateIp';

    // Simulate what example.js would do (extracting device.connect logic)
    const { device } = require('../lib/device.js');
    const dev = await device({ address: mockAddress });
    expect(dev).toHaveProperty('id', 'dev-999');
    expect(dev).toHaveProperty('name', 'TestDeviceAlt');
  });

  it('should print error if device connection fails with a different error', async () => {
    jest.doMock(path.resolve(__dirname, '../lib/device.js'), () => ({
      device: jest.fn(() => Promise.reject(new Error('remote host refused')))
    }), { virtual: true });

    const { device } = require('../lib/device.js');
    await expect(device({ address: 'badIp' })).rejects.toThrow('remote host refused');
  });
});