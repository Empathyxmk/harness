const postcss = require('postcss');
const lh = require('../src/lib/lh');

// Helper for processing CSS
function process(css, opts = {}) {
  return postcss([lh(opts)]).process(css, { from: undefined });
}

describe("lh plugin", () => {
  it("converts lh units to rem using default line height", async () => {
    const input = ".foo { margin-top: 2lh; }";
    const result = await process(input);
    expect(result.css).toMatch(/3rem/); // 2*1.5 = 3
  });

  it("uses custom line-height from :root", async () => {
    const css = `
    :root { line-height: 2; }
    .bar { padding: 1lh; }
    `;
    const result = await process(css);
    expect(result.css).toMatch(/2rem/); // 1*2
  });

  it("parses font shorthand with line-height", async () => {
    const css = `
    :root { font: 1rem/2.2 Arial; }
    .baz { margin-bottom: 1lh; }
    `;
    const result = await process(css);
    expect(result.css).toMatch(/2.2rem/);
  });

  it("ignores print media queries", async () => {
    const css = `
    @media print {
      :root { line-height: 4; }
    }
    .box { margin: 2lh; }
    `;
    const result = await process(css);
    expect(result.css).toMatch(/3rem/); // Should fallback to default 1.5*2 = 3
  });

  it("uses unit passed in opts", async () => {
    const css = `.a { padding: 5foo; }`;
    const result = await postcss([lh({ unit: "foo", lineHeight: 2 })]).process(css, { from: undefined });
    expect(result.css).toMatch(/10rem/);
  });

  it("handles no matches", async () => {
    const css = `.b { color: red; }`;
    const result = await process(css);
    expect(result.css).toContain('red');
  });
});