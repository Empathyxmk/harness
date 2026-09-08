const fs = require('fs');
const path = require('path');

describe('grammar.js syntax', () => {
  let src;
  beforeAll(() => {
    src = fs.readFileSync(path.join(__dirname, 'grammar.js'), 'utf8');
  });

  it('should export using module.exports and define grammar(', () => {
    expect(src).toMatch(/module\.exports\s*=\s*grammar\s*\(/);
  });

  it('should declare a name property', () => {
    expect(src).toMatch(/name\s*:\s*['"`]vhs['"`]/);
  });

  it('should define rules', () => {
    expect(src).toMatch(/rules\s*:\s*\{/);
    // Check 'program' is defined as root rule
    expect(src).toMatch(/program\s*:/);
    // Check at least one command, e.g. 'command:'
    expect(src).toMatch(/command\s*:/);
  });

  it('should have at least one regular expression rule', () => {
    expect(src).toMatch(/\/[^/]+\/[gimsuy]*/); // looks for regexp
  });
});

// Functional test using tree-sitter if available
let Parser, VHS;
try {
  Parser = require('tree-sitter');
  VHS = require('./grammar.js');
} catch (e) {
  // tree-sitter not installed, skip functional tests
}

(Parser && VHS ? describe : describe.skip)('Functional (if tree-sitter installed) VHS grammar', () => {
  it('should parse a basic file without errors', () => {
    const parser = new Parser();
    parser.setLanguage(VHS);
    const tree = parser.parse('echo hello\n# a comment\n');
    expect(tree.rootNode.type).toBe('program');
    expect(tree.rootNode.namedChildCount).toBeGreaterThan(0);
  });

  it('should match a sequence of commands and comments', () => {
    const parser = new Parser();
    parser.setLanguage(VHS);
    const sample = 'Type "Hello"\n# Comment\nOutput file.txt\nSleep 1s\n';
    const tree = parser.parse(sample);
    expect(tree.rootNode.namedChildCount).toBeGreaterThan(1);
  });

  it('should support a wide variety of VHS constructs', () => {
    const parser = new Parser();
    parser.setLanguage(VHS);
    const sample = [
      'Ctrl+Alt+Delete',
      'Alt+Tab',
      'Shift+Z',
      'Set Shell "bash"',
      'Env FOO "bar"',
      'Sleep 2.5s',
      'Type @123 "asdf"',
      'Backspace @400 2',
      'Down',
      'Enter',
      'Escape',
      'Left',
      'Right',
      'Space',
      'Tab',
      'Up',
      'PageUp',
      'PageDown',
      'Wait +Screen @100 /regex/',
      'Require "tree-sitter"',
      'Source "foo.vhs"',
      'Set FontSize 15.5',
      'Set Framerate 30',
      'Set Theme {"bg":"dark"}',
      'Set TypingSpeed 1.2s',
      '# support line comment',
      'Output path/file.txt'
    ].join('\n');
    const tree = parser.parse(sample);
    expect(tree.rootNode.namedChildCount).toBeGreaterThan(10);
  });
});