// tests/whitespace.test.js
const { checkMarkdownWhitespace } = require('../whitespace');
const fs = require('fs');

// Write a temporary markdown file for testing
const testMdPath = './tests/tmp_test.md';

describe('checkMarkdownWhitespace', () => {
  afterAll(() => {
    if (fs.existsSync(testMdPath)) fs.unlinkSync(testMdPath);
  });

  it('returns pass on well-formed markdown', async () => {
    fs.writeFileSync(testMdPath, '# Hello\nNo trailing whitespace\n');
    const result = await checkMarkdownWhitespace([testMdPath], './tests/relaxed.json');
    expect(result.passed).toBe(true);
    expect(result.result).toBe('Pass');
  });

  it('returns fail on markdown with trailing spaces', async () => {
    fs.writeFileSync(testMdPath, '# Bad line  \nTrailing whitespace!   \n');
    const result = await checkMarkdownWhitespace([testMdPath], './tests/relaxed.json');
    expect(result.passed).toBe(false);
    expect(result.result.length).toBeGreaterThan(1);
  });

  it('returns error on missing file', async () => {
    await expect(checkMarkdownWhitespace(['./no_such_file.md'], './tests/relaxed.json')).rejects.toBeTruthy();
  });
});