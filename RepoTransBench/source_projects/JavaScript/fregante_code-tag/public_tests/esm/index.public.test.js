// Use dynamic import for ESM compatibility in Jest
describe('concatenateTemplateLiteralTag/any and aliases (public)', () => {
  let any, html, css, gql, graphql, md, markdown, sql;
  beforeAll(async () => {
    const m = await import('../../esm/index.js');
    any = m.any;
    html = m.html;
    css = m.css;
    gql = m.gql;
    graphql = m.graphql;
    md = m.md;
    markdown = m.markdown;
    sql = m.sql;
  });

  test('returns raw[0] when no keys are provided (public)', () => {
    expect(any`Public test`).toBe('Public test');
  });

  test('returns interpolated string when keys are provided (public)', () => {
    const age = 25;
    expect(any`I am ${age} years old.`).toBe('I am 25 years old.');
  });

  test('html alias works the same as any (public)', () => {
    expect(html`<span>${5 * 3}</span>`).toBe('<span>15</span>');
  });

  test('css alias works with template literals (public)', () => {
    expect(css`.container { width: ${'100%'}; }`).toBe('.container { width: 100%; }');
  });

  test('gql alias works (public)', () => {
    expect(gql`mutation { addUser(name: "Alice") }`).toBe('mutation { addUser(name: "Alice") }');
  });

  test('graphql alias works (public)', () => {
    expect(graphql`query getUser { name }`).toBe('query getUser { name }');
  });

  test('md alias works (public)', () => {
    expect(md`## Subheader`).toBe('## Subheader');
  });

  test('markdown alias works (public)', () => {
    expect(markdown`1. First item`).toBe('1. First item');
  });

  test('sql alias works (public)', () => {
    expect(sql`UPDATE users SET name='Bob' WHERE id=${42}`).toBe("UPDATE users SET name='Bob' WHERE id=42");
  });

  test('empty template returns empty string (public)', () => {
    expect(any``).toBe('');
  });

  test('multiple interpolations (public)', () => {
    const x = 'X', y = 'Y', z = 'Z';
    expect(any`${x},${y},${z}`).toBe('X,Y,Z');
  });
});