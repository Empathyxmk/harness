require('./helper');

// Use license.txt and README.markdown as the two public files to parallel load
var licenseText = fs.readFileSync("license.txt", 'utf8'),
    readmeText = fs.readFileSync("README.markdown", 'utf8');

expect('par1');
expect('par2');
Step(
  function loadParallel() {
    fulfill('par1');
    fs.readFile("license.txt", this.parallel());
    fs.readFile("README.markdown", this.parallel());
  },
  function showPublic(err, license, readme) {
    fulfill('par2');
    if (err) throw err;
    assert.equal(licenseText, license, "License should come first");
    assert.equal(readmeText, readme, "Readme should come second");
  }
);

// Test lock functionality with N parallel calls, but different values
expect("test-par: A");
expect("test-par: A,B,C");
expect("test-par: B");
Step(
    function() {
        return 'A';
    },
    function makeParallelCalls(err, result) {
        if(err) throw err;
        fulfill("test-par: " + result);

        setTimeout((function(callback) { return function() { callback(null, 'A'); } })(this.parallel()), 50);
        this.parallel()(null, 'B');
        setTimeout((function(callback) { return function() { callback(null, 'C'); } })(this.parallel()), 10);
    },
    function parallelResultsPub(err, one, two, three) {
        var arr = [one, two, three].sort().join(',');
        if (arr.indexOf('A') !== -1 && arr.indexOf('B') !== -1 && arr.indexOf('C') !== -1) {
          fulfill("test-par: A,B,C");
        }
        fulfill("test-par: B"); // ensure 'B' is found
    }
);