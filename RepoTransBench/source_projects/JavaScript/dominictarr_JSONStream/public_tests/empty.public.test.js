var JSONStream = require('../');
var it = require('it-is');

exports['parse empty array'] = function (test) {
  var parser = JSONStream.parse();
  var results = [];

  parser.on('data', function (data) {
    results.push(data);
  });
  parser.on('end', function () {
    it(results).deepEqual([[]]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write('[]');
  parser.end();
};

exports['parse empty object'] = function (test) {
  var parser = JSONStream.parse();
  var results = [];

  parser.on('data', function (data) {
    results.push(data);
  });
  parser.on('end', function () {
    it(results).deepEqual([{}]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write('{}');
  parser.end();
};