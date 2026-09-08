// public_tests/whitespace.public.test.js
const { checkMarkdownWhitespace } = require('../whitespace');
const fs = require('fs');

const testMdPath = './public_tests/tmp_public_test.md';

describe('checkMarkdownWhitespace (PUBLIC)', () => {
  afterAll(() => {
    if (fs.existsSync(testMdPath)) fs.unlinkSync(testMdPath);
  });

  it('returns pass on well-formed markdown with variation', async () => {
    // Variation: use a different heading and no trailing whitespace
    fs.writeFileSync(testMdPath, '## Welcome\nClean content line.\n');
    const result = await checkMarkdownWhitespace([testMdPath], './tests/relaxed.json');
    expect(result.passed).toBe(true);
    expect(result.result).toBe('Pass');
  });

  it('returns fail on markdown with different trailing whitespace', async () => {
    // Variation: 1 space on one line, 3 spaces on another
    fs.writeFileSync(testMdPath, 'Just a line \nAnother bad line   \n');
    const result = await checkMarkdownWhitespace([testMdPath], './tests/relaxed.json');
    expect(result.passed).toBe(false);
    expect(result.result.length).toBeGreaterThan(1);
  });

  it('returns error on missing file with different file name', async () => {
    await expect(checkMarkdownWhitespace(['./definitely_missing_file.md'], './tests/relaxed.json')).rejects.toBeTruthy();
  });
});