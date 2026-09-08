import parseOptions from '../src/parse-options';

describe('Option filter public tests for plugin', () => {
  it('can be called with different option values', () => {
    expect(typeof parseOptions).toBe('function');
    expect(() => parseOptions({ maxEmptyLines: 7, comments: 'all' })).not.toThrow();
  });
});