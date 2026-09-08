// Remove chai, use plain assertions to avoid CommonJS/ESM conflicts
describe('Environment Smoke Test', function() {
  it('should add numbers', function() {
    if (1 + 1 !== 2) {
      throw new Error('Math is broken');
    }
  });
});