const postcss = require('postcss');
const lh = require('../src/lib/lh');

// Helper for processing CSS
function process(css, opts = {}) {
  return postcss([lh(opts)]).process(css, { from: undefined });
}

describe("lh plugin PUBLIC TEST", () => {
  it("converts lh units to rem using a different default line height", async () => {
    // Use 3lh instead of 2lh for input value
    const input = ".foo { margin-top: 3lh; }";
    const result = await process(input);
    expect(result.css).toMatch(/4.5rem/); // 3*1.5 = 4.5
  });

  it("uses custom line-height from :root with a different value", async () => {
    const css = `
    :root { line-height: 1.7; }
    .bar { padding: 2lh; }
    `;
    const result = await process(css);
    expect(result.css).toMatch(/3.4rem/); // 2*1.7 = 3.4
  });

  it("parses font shorthand with line-height (public different value)", async () => {
    const css = `
    :root { font: 1.1rem/2.5 Helvetica; }
    .baz { margin-bottom: 2lh; }
    `;
    const result = await process(css);
    expect(result.css).toMatch(/5rem/); // 2*2.5 = 5
  });

  it("ignores print media queries with different input", async () => {
    const css = `
    @media print {
      :root { line-height: 3.5; }
    }
    .box { margin: 2lh; }
    `;
    const result = await process(css);
    expect(result.css).toMatch(/3rem/); // Should fallback to default 1.5*2 = 3
  });

  it("uses unit passed in opts with different numbers", async () => {
    const css = `.a { padding: 3bar; }`;
    const result = await postcss([lh({ unit: "bar", lineHeight: 4 })]).process(css, { from: undefined });
    expect(result.css).toMatch(/12rem/); // 3*4
  });

  it("handles no matches differently", async () => {
    const css = `.c { color: blue; }`; // changed from 'red'
    const result = await process(css);
    expect(result.css).toContain('blue');
  });
});