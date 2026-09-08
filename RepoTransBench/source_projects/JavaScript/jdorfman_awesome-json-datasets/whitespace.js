// whitespace.js
// Extracts the main check from whitespace_test.js for coverage and testability
const markdownlint = require("markdownlint");

function checkMarkdownWhitespace(files = ['./README.md'], configPath = './tests/relaxed.json') {
  return new Promise((resolve, reject) => {
    let options = {
      files,
      config: require(configPath)
    };
    markdownlint(options, function callback(err, result) {
      if (err) {
        reject(err);
      } else if (result.toString().length > 1) {
        resolve({ passed: false, result: result.toString() });
      } else {
        resolve({ passed: true, result: 'Pass' });
      }
    });
  });
}

module.exports = { checkMarkdownWhitespace };