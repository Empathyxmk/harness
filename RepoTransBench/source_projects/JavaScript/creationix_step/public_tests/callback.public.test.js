require('./helper');

// Use a *different* file for content testing to change test data.
// We'll use the license.txt file (license.txt always present, distinct from __filename in existing test).

var licenseText = fs.readFileSync("license.txt", 'utf8');

// Testing Step passing async/sync results to next layer
expect('uno');
expect('dos');
expect('tres');
Step(
  function readLicense() {
    fulfill("uno");
    fs.readFile("license.txt", 'utf8', this);
  },
  function capitalize(err, text) {
    fulfill("dos");
    if (err) throw err;
    assert.equal(licenseText, text, "License Text Loaded");
    return text.split('').reverse().join('');
  },
  function showIt(err, newText) {
    fulfill("tres");
    if (err) throw err;
    assert.equal(licenseText.split('').reverse().join(''), newText, "License Text Reversed");
  }
);