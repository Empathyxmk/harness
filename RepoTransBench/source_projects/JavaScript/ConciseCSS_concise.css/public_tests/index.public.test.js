const fs = require("fs");
const path = require('path');
const test = require('tape');
const postcss = require('postcss');
const concise = require('../src/index.js');

;(() => {
  const actual = async file => {
    const sourcePath = path.join(__dirname,`../test/fixtures/${file}/${file}.pcss`);
    const fileContent = fs.readFileSync(sourcePath, 'utf8');

    const result = await postcss([concise]).process(fileContent, { from: sourcePath });

    return result.css.replace(/\s+/g, '');
  };

  const expected = (file) =>
    fs.readFileSync(
      path.join(__dirname, `../test/fixtures/${file}/${file}.css`),
      'utf8'
    ).replace(/\s+/g, '');

  test('Media queries (public test)', async (t) => {
    // swap order and call again for coverage, but check for correctness.
    t.equal(
      await actual('mediaMinMax'),
      expected('mediaMinMax'),
      'Ranges in media queries (different order)'
    );

    t.equal(
      await actual('customMedia'),
      expected('customMedia'),
      'Custom media queries (different order)'
    );

    t.end();
  });

  test('Units (public test)', async (t) => {
    // Re-run verticalRhythm as in original test for public coverage
    t.equal(
      await actual('verticalRhythm'),
      expected('verticalRhythm'),
      'lh (public)'
    );

    t.end();
  });
})();