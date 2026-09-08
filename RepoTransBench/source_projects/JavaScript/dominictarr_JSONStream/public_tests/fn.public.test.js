var JSONStream = require('../');
var it = require('it-is');

exports['parse with replace function for numbers'] = function (test) {
  var data = '{"x":50,"y":25,"z":75}';
  var parser = JSONStream.parse('*', function (value, key) {
    // Replace with incremented value
    if (typeof value === 'number') return value + 5;
    return value;
  });
  var results = [];

  parser.on('data', function (val) { results.push(val); });
  parser.on('end', function () {
    it(results).deepEqual([55, 30, 80]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(data);
  parser.end();
};

exports['parse with object-wide replace function'] = function (test) {
  var data = '{"a":1,"b":2}';
  var parser = JSONStream.parse(undefined, function (value, key) {
    if (typeof value === 'object' && value && value.a) {
      value.c = value.a + value.b;
    }
    return value;
  });
  var results = [];

  parser.on('data', function (val) { results.push(val); });
  parser.on('end', function () {
    it(results).deepEqual([{ a: 1, b: 2, c: 3 }]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(data);
  parser.end();
};