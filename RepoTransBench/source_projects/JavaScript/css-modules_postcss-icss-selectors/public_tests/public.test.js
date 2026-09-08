const postcss = require("postcss");
const icssSelect = require("../src/index.js");

// Note: These test cases use different data, but test the same plugin logic as test/test.js.

describe("postcss-icss-selectors public test suite", () => {
  it("should rewrite selectors with :icss-selector (public test)", async () => {
    const input = `
      :icss-selector {
        -icss-selector: .publicClass;
      }
      .publicClass {
        color: blue;
      }
    `;
    const expected = `
      .publicClass {
        color: blue;
      }
    `;
    const result = await postcss([icssSelect()]).process(input, { from: undefined });
    expect(result.css.replace(/\s+/g, " ")).toBe(expected.replace(/\s+/g, " "));
  });

  it("should rewrite multiple selectors (public test)", async () => {
    const input = `
      :icss-selector {
        -icss-selector: .x;
      }
      .x .y {
        background: yellow;
      }
      :icss-selector {
        -icss-selector: #different;
      }
      #different .footer {
        color: pink;
      }
    `;
    // All rules are rewritten to begin with the last selector: #different
    const expected = `
      #different .y {
        background: yellow;
      }
      #different .footer {
        color: pink;
      }
    `;
    const result = await postcss([icssSelect()]).process(input, { from: undefined });
    expect(result.css.replace(/\s+/g, " ")).toBe(expected.replace(/\s+/g, " "));
  });

  it("removes :icss-selector block (public test)", async () => {
    const input = `
      :icss-selector {
        -icss-selector: .gamma;
      }
      .gamma {
        font-weight: bold;
      }
      .delta {
        font-style: italic;
      }
    `;
    // All rules are rewritten to begin with .gamma due to plugin logic
    const expected = `
      .gamma {
        font-weight: bold;
      }
      .gamma {
        font-style: italic;
      }
    `;
    const result = await postcss([icssSelect()]).process(input, { from: undefined });
    expect(result.css.replace(/\s+/g, " ")).toBe(expected.replace(/\s+/g, " "));
  });
});