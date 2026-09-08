var JSONStream = require('../');
var it = require('it-is');

exports['parse single boolean values'] = function (test) {
  var parser = JSONStream.parse();
  var results = [];

  parser.on('data', function (data) {
    results.push(data);
  });
  parser.on('end', function () {
    it(results).deepEqual([false]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write('false');
  parser.end();
};

// Diverse booleans set:
exports['parse multiple booleans'] = function (test) {
  var parser = JSONStream.parse();
  var results = [];

  parser.on('data', function (data) {
    results.push(data);
  });
  parser.on('end', function () {
    it(results).deepEqual([false, true, false]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write('false');
  parser.write('true');
  parser.write('false');
  parser.end();
};