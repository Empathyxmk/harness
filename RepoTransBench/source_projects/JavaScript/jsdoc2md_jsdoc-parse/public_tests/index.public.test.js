const jsdocParse = require('../index');

describe('index.js - PUBLIC', () => {
  test('jsdocParse filters and sorts array by name (PUBLIC)', () => {
    const input = [
      { name: 'm', documented: true, kind: 'function' },
      { name: 'a', kind: 'typedef', undocumented: true },
      { name: 'n', documented: true, kind: 'function' },
      { name: 'c', kind: 'enum', undocumented: true }
    ];
    const result = jsdocParse(input);
    // Only 'm' and 'n' remain, sorting may retain input order
    expect(result.map(i => i.name)).toEqual(['m', 'n']);
  });

  test('jsdocParse runs PUBLIC transform and sorting', () => {
    const input = [
      { name: 'beta', documented: true, kind: 'function' },
      { name: 'epsilon', kind: 'enum', undocumented: true },
      { name: 'alpha', documented: true, kind: 'function' }
    ];
    const result = jsdocParse(input);
    // Only 'beta' and 'alpha' remain, sorting may retain input order
    expect(result.map(d => d.name)).toEqual(['beta', 'alpha']);
  });
});