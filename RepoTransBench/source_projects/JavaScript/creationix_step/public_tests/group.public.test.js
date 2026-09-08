require('./helper');

// Use test/ as our alternate directory and read files (instead of __dirname from test/groupTest.js)
var testDir = "test";
var testListing = fs.readdirSync(testDir),
    testResults = testListing.map(function (filename) {
      return fs.readFileSync(testDir + "/" + filename, 'utf8');
    });

expect('g1');
expect('g2');
expect('g3');
Step(
  function readDirAlt() {
    fulfill('g1');
    fs.readdir(testDir, this);
  },
  function readFilesAlt(err, results) {
    fulfill('g2');
    if (err) throw err;
    assert.deepEqual(testListing, results);
    var group = this.group();
    results.forEach(function (filename) {
      if (/\.js$/.test(filename)) {
        fs.readFile(testDir + "/" + filename, 'utf8', group());
      }
    });
  },
  function showAllAlt(err , files) {
    fulfill('g3');
    if (err) throw err;
    assert.deepEqual(testResults, files);
  }
);

// When the group is empty, it should fire with an empty array
expect('g4');
expect('g5');
Step(
  function startAlt() {
    var group = this.group();
    // No calls to group()
    fulfill('g4');
  },
  function doneAlt(err, results) {
    // Immediate fire with empty
    fulfill('g5');
    assert.deepEqual([], results);
  }
);