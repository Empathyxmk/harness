// The original suite was using Mocha/Jasmine syntax (`describe`, `it`), but other public tests use tap-style exports.
// Let's use tap-compatible module exports for this context, matching the other test style.

var JSONStream = require('../');
var it = require('it-is');

exports['roundtrip parse and stringify with alternative data'] = function(test) {
  var input = [
    {a: 5, b: 7},
    {a: 0, b: 14}
  ];

  var stringify = JSONStream.stringify();
  var parse = JSONStream.parse('*');
  var output = [];

  stringify.pipe(parse);

  parse.on('data', function(obj) {
    output.push(obj);
  });

  parse.on('end', function() {
    it(output).deepEqual(input);
    if (test && typeof test.done === 'function') test.done();
  });

  input.forEach(function(item) {
    stringify.write(item);
  });
  stringify.end();
};