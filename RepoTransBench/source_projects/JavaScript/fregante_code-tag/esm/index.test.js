// Use dynamic import for ESM compatibility in Jest
describe('concatenateTemplateLiteralTag/any and aliases', () => {
  let any, html, css, gql, graphql, md, markdown, sql;
  beforeAll(async () => {
    const m = await import('./index.js');
    any = m.any;
    html = m.html;
    css = m.css;
    gql = m.gql;
    graphql = m.graphql;
    md = m.md;
    markdown = m.markdown;
    sql = m.sql;
  });

  test('returns raw[0] when no keys are provided', () => {
    expect(any`Hello world!`).toBe('Hello world!');
  });

  test('returns interpolated string when keys are provided', () => {
    const name = 'world';
    expect(any`Hello ${name}!`).toBe('Hello world!');
  });

  test('html alias works the same as any', () => {
    expect(html`<div>${1 + 1}</div>`).toBe('<div>2</div>');
  });

  test('css alias works with template literals', () => {
    expect(css`.a { color: ${'red'}; }`).toBe('.a { color: red; }');
  });

  test('gql alias works', () => {
    expect(gql`query { hello }`).toBe('query { hello }');
  });

  test('graphql alias works', () => {
    expect(graphql`fragment user on User { id }`).toBe('fragment user on User { id }');
  });

  test('md alias works', () => {
    expect(md`# Header`).toBe('# Header');
  });

  test('markdown alias works', () => {
    expect(markdown`* Bullet`).toBe('* Bullet');
  });

  test('sql alias works', () => {
    expect(sql`SELECT * FROM users WHERE id=${1}`).toBe('SELECT * FROM users WHERE id=1');
  });

  test('empty template returns empty string', () => {
    expect(any``).toBe('');
  });

  test('multiple interpolations', () => {
    const a = 'A', b = 'B', c = 'C';
    expect(any`${a} ${b} ${c}`).toBe('A B C');
  });
});