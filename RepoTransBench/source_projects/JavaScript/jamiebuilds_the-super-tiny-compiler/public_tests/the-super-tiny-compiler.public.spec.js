const {
  tokenizer,
  parser,
  transformer,
  codeGenerator,
  compiler,
} = require('../the-super-tiny-compiler');

describe("tokenizer (public)", () => {
  test("tokenizes parens, name, and numbers - different data", () => {
    const input = "(multiply 3 7)";
    expect(tokenizer(input)).toEqual([
      { type: "paren", value: "(" },
      { type: "name", value: "multiply" },
      { type: "number", value: "3" },
      { type: "number", value: "7" },
      { type: "paren", value: ")" }
    ]);
  });

  test("tokenizes different names and numbers with multi-digits", () => {
    const input = "(bar789 987foo)";
    expect(tokenizer(input)).toEqual([
      { type: "paren", value: "(" },
      { type: "name", value: "bar" },
      { type: "number", value: "789" },
      { type: "number", value: "987" },
      { type: "name", value: "foo" },
      { type: "paren", value: ")" }
    ]);
  });
});

describe("parser (public)", () => {
  test("parses basic multiply expression", () => {
    const tokens = [
      { type: "paren", value: "(" },
      { type: "name", value: "multiply" },
      { type: "number", value: "3" },
      { type: "number", value: "7" },
      { type: "paren", value: ")" }
    ];
    expect(parser(tokens)).toEqual({
      type: "Program",
      body: [
        {
          type: "CallExpression",
          name: "multiply",
          params: [
            { type: "NumberLiteral", value: "3" },
            { type: "NumberLiteral", value: "7" }
          ]
        }
      ]
    });
  });
});

describe("transformer (public)", () => {
  test("transforms CallExpression to ExpressionStatement - different data", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "CallExpression",
          name: "multiply",
          params: [
            { type: "NumberLiteral", value: "3" },
            { type: "NumberLiteral", value: "7" }
          ]
        }
      ]
    };
    expect(transformer(ast)).toEqual({
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: {
            type: "CallExpression",
            callee: { type: "Identifier", name: "multiply" },
            arguments: [
              { type: "NumberLiteral", value: "3" },
              { type: "NumberLiteral", value: "7" }
            ]
          }
        }
      ]
    });
  });
});

describe("codeGenerator (public)", () => {
  test("generates code for multiply", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: {
            type: "CallExpression",
            callee: { type: "Identifier", name: "multiply" },
            arguments: [
              { type: "NumberLiteral", value: "3" },
              { type: "NumberLiteral", value: "7" }
            ]
          }
        }
      ]
    };
    expect(codeGenerator(ast)).toBe("multiply(3, 7);");
  });
  test("generates code for number - different value", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: { type: "NumberLiteral", value: "15" }
        }
      ]
    };
    expect(codeGenerator(ast)).toBe("15;");
  });
});

describe("compiler integration (public)", () => {
  test("compiles input to output - different data", () => {
    const input = "(multiply 3 (divide 10 2))";
    const output = "multiply(3, divide(10, 2));";
    expect(compiler(input)).toBe(output);
  });
});