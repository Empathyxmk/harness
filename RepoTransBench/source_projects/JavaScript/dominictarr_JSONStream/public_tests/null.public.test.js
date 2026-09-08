var JSONStream = require('../');
var it = require('it-is');

exports['parse null value'] = function (test) {
  var parser = JSONStream.parse();
  var results = [];

  parser.on('data', function (data) {
    results.push(data);
  });
  parser.on('end', function () {
    it(results).deepEqual([null]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write('null');
  parser.end();
};

exports['parse array with nulls/booleans'] = function (test) {
  var parser = JSONStream.parse();
  var results = [];

  parser.on('data', function (data) {
    results.push(data);
  });
  parser.on('end', function () {
    it(results).deepEqual([[false, null, true, null]]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write('[false,null,true,null]');
  parser.end();
};