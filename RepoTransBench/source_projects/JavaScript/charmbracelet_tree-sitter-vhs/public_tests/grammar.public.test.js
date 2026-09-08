const fs = require('fs');
const path = require('path');

describe('grammar.js structure (public)', () => {
  let src;
  beforeAll(() => {
    src = fs.readFileSync(path.join(__dirname, '../grammar.js'), 'utf8');
  });

  it('should use module.exports and reference grammar keyword', () => {
    // Use slightly different match test
    expect(src.startsWith('module.exports')).toBe(true);
    expect(src.includes('grammar(')).toBe(true);
  });

  it('should contain "vhs" as the language name', () => {
    // Use different quote type, and more precise test
    expect(/name\s*:\s*['"`]vhs['"`]/.test(src)).toBe(true);
  });

  it('should mention rules object with at least two VHS rules (public check)', () => {
    expect(src.includes('rules')).toBe(true);
    expect(src.includes('env:')).toBe(true);
    expect(src.includes('type:')).toBe(true);
  });

  it('should have at least one RegExp literal in rules', () => {
    // Find a regexp not matching the exact text in the original test
    expect(/\/[A-Za-z+\\]+\/[a-z]?/.test(src)).toBe(true);
  });
});

// Functional public test using tree-sitter if available
let Parser, VHS;
try {
  Parser = require('tree-sitter');
  VHS = require('../grammar.js');
} catch (e) {
  // tree-sitter not installed, skip functional tests
}

(Parser && VHS ? describe : describe.skip)('Functional VHS grammar (public data)', () => {
  it('should parse an alternate program with various VHS commands', () => {
    const parser = new Parser();
    parser.setLanguage(VHS);
    const tree = parser.parse('Output "example.txt"\n# comment line\n');
    expect(tree.rootNode.type).toBe('program');
    expect(tree.rootNode.namedChildCount).toBeGreaterThan(0);
  });

  it('should parse a different mix of commands and comments', () => {
    const parser = new Parser();
    parser.setLanguage(VHS);
    const sample = 'Set Shell "zsh"\n# Another comment\nBackspace @100 5\nSleep 0.75s\n';
    const tree = parser.parse(sample);
    expect(tree.rootNode.namedChildCount).toBeGreaterThan(1);
  });

  it('should support additional VHS constructs with public data', () => {
    const parser = new Parser();
    parser.setLanguage(VHS);
    const sample = [
      'Ctrl+Shift+Enter',
      'Alt+Shift+Tab',
      'Set FontFamily "Fira Mono"',
      'Set PlaybackSpeed 1.5',
      'Set Height 40',
      'Set Padding 2.25',
      'Type @456 "publicTest"',
      'Down @200 3',
      'Up',
      'PageUp @300 2',
      'Set WindowBarSize 18',
      'Set CursorBlink true',
      'Env USER "jdoe"',
      'Require "custom-parser"',
      'Source "public.vhs"',
      '# A different kind of comment',
      'Sleep 3s'
    ].join('\n');
    const tree = parser.parse(sample);
    expect(tree.rootNode.namedChildCount).toBeGreaterThan(10);
  });
});