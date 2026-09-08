require('./helper');

// Use a different existing file for this public case: README.markdown
var pubfn = Step.fn(
  function (name) {
    fs.readFile(name, 'utf8', this);
  },
  function capitalize(err, text) {
    if (err) throw err;
    return text.toLowerCase(); // Change from toUpperCase
  }
);

var readmeText = fs.readFileSync("README.markdown", 'utf8');

expect('result-pub');
pubfn("README.markdown", function (err, output) {
  fulfill('result-pub');
  if (err) throw err;
  assert.equal(readmeText.toLowerCase(), output, "It should transform to lower");
});