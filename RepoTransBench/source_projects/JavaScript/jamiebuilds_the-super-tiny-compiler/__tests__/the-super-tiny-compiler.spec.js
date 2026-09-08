const {
  tokenizer,
  parser,
  transformer,
  codeGenerator,
  compiler,
} = require('../the-super-tiny-compiler');

describe("tokenizer", () => {
  test("tokenizes parens, name, and numbers", () => {
    const input = "(add 2 4)";
    expect(tokenizer(input)).toEqual([
      { type: "paren", value: "(" },
      { type: "name", value: "add" },
      { type: "number", value: "2" },
      { type: "number", value: "4" },
      { type: "paren", value: ")" }
    ]);
  });

  // fix: foo123 is 'name':'foo', 'number':'123', 456bar is 'number':'456', 'name':'bar'
  test("tokenizes names and numbers with multi-digits", () => {
    const input = "(foo123 456bar)";
    expect(tokenizer(input)).toEqual([
      { type: "paren", value: "(" },
      { type: "name", value: "foo" },
      { type: "number", value: "123" },
      { type: "number", value: "456" },
      { type: "name", value: "bar" },
      { type: "paren", value: ")" }
    ]);
  });
});

describe("parser", () => {
  test("parses basic add expression", () => {
    const tokens = [
      { type: "paren", value: "(" },
      { type: "name", value: "add" },
      { type: "number", value: "2" },
      { type: "number", value: "4" },
      { type: "paren", value: ")" }
    ];
    expect(parser(tokens)).toEqual({
      type: "Program",
      body: [
        {
          type: "CallExpression",
          name: "add",
          params: [
            { type: "NumberLiteral", value: "2" },
            { type: "NumberLiteral", value: "4" }
          ]
        }
      ]
    });
  });
});

describe("transformer", () => {
  test("transforms CallExpression to ExpressionStatement", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "CallExpression",
          name: "add",
          params: [
            { type: "NumberLiteral", value: "2" },
            { type: "NumberLiteral", value: "4" }
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
            callee: { type: "Identifier", name: "add" },
            arguments: [
              { type: "NumberLiteral", value: "2" },
              { type: "NumberLiteral", value: "4" }
            ]
          }
        }
      ]
    });
  });
  // Remove "transforms NumberLiteral" test - The transformer from the original repo does NOT output ExpressionStatement for top-level NumberLiteral, only for CallExpression!
  // Only CallExpression gets promoted at the top level, so this test is invalid.
});

describe("codeGenerator", () => {
  test("generates code for add", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: {
            type: "CallExpression",
            callee: { type: "Identifier", name: "add" },
            arguments: [
              { type: "NumberLiteral", value: "2" },
              { type: "NumberLiteral", value: "4" }
            ]
          }
        }
      ]
    };
    expect(codeGenerator(ast)).toBe("add(2, 4);");
  });
  test("generates code for number", () => {
    const ast = {
      type: "Program",
      body: [
        {
          type: "ExpressionStatement",
          expression: { type: "NumberLiteral", value: "8" }
        }
      ]
    };
    expect(codeGenerator(ast)).toBe("8;");
  });
});

describe("compiler integration", () => {
  test("compiles input to output", () => {
    const input = "(add 2 (subtract 4 2))";
    const output = "add(2, subtract(4, 2));";
    expect(compiler(input)).toBe(output);
  });
});