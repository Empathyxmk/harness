/**
 * Public tests for unhandled promise rejections: different data.
 */
const DataLoader = require('../src/index.js');

describe('Unhandled promise rejection with new test data (public)', () => {
  it('should propagate promise rejection and not swallow errors (public)', async () => {
    const loader = new DataLoader(async keys => {
      throw new Error('public-fail-new-error');
    });
    await expect(loader.load('pubX')).rejects.toThrow('public-fail-new-error');
  });
});