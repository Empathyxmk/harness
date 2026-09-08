const postcss = require('postcss');
const typeScale = require('../src/lib/type-scale');

// Helper for processing CSS
function process(css, opts = {}) {
  return postcss([typeScale(opts)]).process(css, { from: undefined });
}

describe("type-scale plugin", () => {
  it("replaces font-size for unitless values", async () => {
    const css = ".foo { font-size: 4; }";
    const result = await process(css);
    // 1.2^(4-2) = 1.44
    expect(result.css).toMatch(/1\.44rem/);
  });

  it("uses --type-ratio from :root", async () => {
    const css = `
    :root { --type-ratio: 1.5; }
    .bar { font-size: 6; }
    `;
    const result = await process(css);
    // 1.5^(6-2) = 5.0625
    expect(result.css).toMatch(/5\.0625rem/);
  });

  it("ignores in print media query", async () => {
    const css = `
    @media print {
      :root { --type-ratio: 2.0; }
    }
    .foo { font-size: 3; }
    `;
    const result = await process(css);
    // Should fallback to default 1.2^(3-2) = 1.2
    expect(result.css).toMatch(/1\.2rem/);
  });

  it("does not replace font-size with units", async () => {
    const css = `.a { font-size: 18px; }`;
    const result = await process(css);
    expect(result.css).toContain("18px");
  });

  it("supports custom option keys", async () => {
    const css = `
    :root { --custom-ratio: 2.2; }
    .b { font-size: 5; }
    `;
    const result = await process(css, { ratioProperty: "--custom-ratio" });
    // 2.2^(5-2) = 10.648
    expect(result.css).toMatch(/10\.648rem/);
  });

  it("handles no matches", async () => {
    const css = `.b { color: blue; }`;
    const result = await process(css);
    expect(result.css).toContain('blue');
  });
});