const postcss = require('postcss');
const typeScale = require('../src/lib/type-scale');

// Helper for processing CSS
function process(css, opts = {}) {
  return postcss([typeScale(opts)]).process(css, { from: undefined });
}

describe("type-scale plugin PUBLIC TEST", () => {
  it("replaces font-size for unitless values with different values", async () => {
    const css = ".foo { font-size: 5; }";
    const result = await process(css);
    // 1.2^(5-2) = 1.728
    expect(result.css).toMatch(/1\.728rem/);
  });

  it("uses --type-ratio from :root with a different value", async () => {
    const css = `
    :root { --type-ratio: 1.3; }
    .bar { font-size: 7; }
    `;
    const result = await process(css);
    // 1.3^(7-2) = 3.71293
    expect(result.css).toMatch(/3\.7129/i); // allow partial match for digits
  });

  it("ignores in print media query with different font-size", async () => {
    const css = `
    @media print {
      :root { --type-ratio: 1.8; }
    }
    .foo { font-size: 4; }
    `;
    const result = await process(css);
    // Should fallback to default 1.2^(4-2) = 1.44
    expect(result.css).toMatch(/1\.44rem/);
  });

  it("does not replace font-size with units (different size)", async () => {
    const css = `.a { font-size: 24px; }`;
    const result = await process(css);
    expect(result.css).toContain("24px");
  });

  it("supports custom option keys with different numbers", async () => {
    const css = `
    :root { --myratio: 1.9; }
    .b { font-size: 3; }
    `;
    const result = await process(css, { ratioProperty: "--myratio" });
    // 1.9^(3-2) = 1.9
    expect(result.css).toMatch(/1\.9rem/);
  });

  it("handles no matches (different color)", async () => {
    const css = `.b { color: green; }`;
    const result = await process(css);
    expect(result.css).toContain('green');
  });
});