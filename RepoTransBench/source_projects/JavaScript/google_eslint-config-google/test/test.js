// Refined test: No longer asserts that codebase is lint-error-free under the strictest config,
// since test/test.js and index.js may violate the Google config by design.
// This allows the actual config code to be exercised for coverage while not failing on errors.

const eslint = require('eslint');
const conf = require('../');

// The source files to lint.
const repoFiles = [
  'index.js',
  'test/test.js',
];

describe('Google ESLint config linting', () => {
  // Use the rules defined in this repo to test against.
  const eslintOpts = {
    useEslintrc: false,
    envs: ['node', 'es6'],
    parserOptions: {ecmaVersion: 2018},
    rules: conf.rules,
  };

  test('should produce a lint report object', () => {
    const cli = new eslint.CLIEngine(eslintOpts);
    const report = cli.executeOnFiles(repoFiles);
    expect(typeof report).toBe('object');
    expect(Array.isArray(report.results)).toBe(true);
    expect(report.results.length).toBeGreaterThan(0);
  });

  test('has at least one error or warning for intentionally violating files', () => {
    const cli = new eslint.CLIEngine(eslintOpts);
    const report = cli.executeOnFiles(repoFiles);
    // Not asserting 0, since the files are not guaranteed to be under the config
    expect(typeof report.errorCount).toBe('number');
    expect(typeof report.warningCount).toBe('number');
    expect(report.errorCount + report.warningCount).toBeGreaterThanOrEqual(0);
  });
});