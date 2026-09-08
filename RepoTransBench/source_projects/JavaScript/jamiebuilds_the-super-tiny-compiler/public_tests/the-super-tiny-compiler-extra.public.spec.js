const {
  tokenizer,
  parser,
  transformer,
  codeGenerator,
  compiler,
} = require('../the-super-tiny-compiler');

describe("tokenizer edge cases (public)", () => {
  test("deeply nested parens (different name)", () => {
    const input = "((((bar))))";
    expect(tokenizer(input)).toEqual([
      { type: "paren", value: "(" },
      { type: "paren", value: "(" },
      { type: "paren", value: "(" },
      { type: "paren", value: "(" },
      { type: "name", value: "bar" },
      { type: "paren", value: ")" },
      { type: "paren", value: ")" },
      { type: "paren", value: ")" },
      { type: "paren", value: ")" }
    ]);
  });
});

describe("parser error and empty handling (public)", () => {
  test("unexpected EOF (different name)", () => {
    const tokens = [
      { type: "paren", value: "(" },
      { type: "name", value: "fooError" }
    ];
    expect(() => parser(tokens)).toThrow();
  });

  test("empty input produces empty program (public)", () => {
    expect(parser([])).toEqual({ type: "Program", body: [] });
  });
});

describe("transformer edge (public)", () => {
  test("strips extra program nodes (public)", () => {
    const ast = {
      type: "Program",
      body: []
    };
    expect(transformer(ast)).toEqual({
      type: "Program",
      body: []
    });
  });
});

describe("codeGenerator (public)", () => {
  test("outputs for empty program (public)", () => {
    expect(codeGenerator({ type: "Program", body: [] })).toBe("");
  });

  test("throws for node with no type (public)", () => {
    expect(() => codeGenerator({})).toThrow();
  });

  test("number with leading zeroes, different value", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: { type: "NumberLiteral", value: "0052" }
        }
      ]
    };
    expect(codeGenerator(ast)).toBe("0052;");
  });
});

describe("compiler (public)", () => {
  test("throws on invalid input (public)", () => {
    expect(() => compiler("(((")).toThrow();
    expect(() => compiler("&badlyFormed")).toThrow();
  });
});