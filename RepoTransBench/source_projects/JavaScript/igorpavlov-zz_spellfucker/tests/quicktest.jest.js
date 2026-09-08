const main = require('./quicktest');

describe('quicktest.js example', () => {
  it('runs demo spellfucker example without crashing', () => {
    const result = main();
    expect(typeof result === 'string' || result instanceof Error).toBe(true);
  });
});