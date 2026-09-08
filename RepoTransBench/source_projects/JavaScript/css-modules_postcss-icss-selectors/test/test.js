const postcss = require("postcss");
const icssSelect = require("../src/index.js");

describe("postcss-icss-selectors core test suite", () => {
  it("should correctly rewrite selectors with :icss-selector", async () => {
    const input = `
      :icss-selector {
        -icss-selector: .myClass;
      }
      .myClass {
        color: red;
      }
    `;
    const expected = `
      .myClass {
        color: red;
      }
    `;
    const result = await postcss([icssSelect()]).process(input, { from: undefined });
    expect(result.css.replace(/\s+/g, " ")).toBe(expected.replace(/\s+/g, " "));
  });

  it("should rewrite multiple selectors", async () => {
    const input = `
      :icss-selector {
        -icss-selector: .a;
      }
      .a .b {
        background: white;
      }
      :icss-selector {
        -icss-selector: #main;
      }
      #main .header {
        color: green;
      }
    `;
    // According to plugin logic, all selectors start with last selector (here, "#main")
    const expected = `
      #main .b {
        background: white;
      }
      #main .header {
        color: green;
      }
    `;
    const result = await postcss([icssSelect()]).process(input, { from: undefined });
    expect(result.css.replace(/\s+/g," ")).toBe(expected.replace(/\s+/g," "));
  });

  it("removes :icss-selector block", async () => {
    const input = `
      :icss-selector {
        -icss-selector: .alpha;
      }
      .alpha {
        font-size: 16px;
      }
      .beta {
        font-size: 12px;
      }
    `;
    // Both rules will start with .alpha (because selector rewriting rule above)
    const expected = `
      .alpha {
        font-size: 16px;
      }
      .alpha {
        font-size: 12px;
      }
    `;
    const result = await postcss([icssSelect()]).process(input, { from: undefined });
    expect(result.css.replace(/\s+/g," ")).toBe(expected.replace(/\s+/g," "));
  });
});