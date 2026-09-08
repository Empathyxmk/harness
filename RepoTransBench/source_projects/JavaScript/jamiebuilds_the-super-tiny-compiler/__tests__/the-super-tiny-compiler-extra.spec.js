const {
  tokenizer,
  parser,
  transformer,
  codeGenerator,
  compiler,
} = require('../the-super-tiny-compiler');

describe("tokenizer edge cases", () => {
  test("deeply nested parens", () => {
    const input = "(((foo)))";
    expect(tokenizer(input)).toEqual([
      { type: "paren", value: "(" },
      { type: "paren", value: "(" },
      { type: "paren", value: "(" },
      { type: "name", value: "foo" },
      { type: "paren", value: ")" },
      { type: "paren", value: ")" },
      { type: "paren", value: ")" }
    ]);
  });

  // See note in spec file about removing tests for unsupported syntax
});

describe("parser error and empty handling", () => {
  test("unexpected EOF", () => {
    const tokens = [
      { type: "paren", value: "(" },
      { type: "name", value: "oops" }
    ];
    expect(() => parser(tokens)).toThrow();
  });

  test("empty input produces empty program", () => {
    expect(parser([])).toEqual({ type: "Program", body: [] });
  });
});

describe("transformer edge", () => {
  test("strips extra program nodes", () => {
    const ast = {
      type: "Program",
      body: []
    };
    expect(transformer(ast)).toEqual({
      type: "Program",
      body: []
    });
  });

  // Remove invalid transformer test for top-level NumberLiteral (not supported by original code)
});

describe("codeGenerator", () => {
  test("outputs for empty program", () => {
    expect(codeGenerator({ type: "Program", body: [] })).toBe("");
  });

  test("throws for node with no type", () => {
    expect(() => codeGenerator({})).toThrow();
  });

  test("number with leading zeroes", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: { type: "NumberLiteral", value: "007" }
        }
      ]
    };
    expect(codeGenerator(ast)).toBe("007;");
  });
});

describe("compiler", () => {
  test("throws on invalid input", () => {
    expect(() => compiler("(")).toThrow();
    expect(() => compiler("$foo")).toThrow();
  });
});