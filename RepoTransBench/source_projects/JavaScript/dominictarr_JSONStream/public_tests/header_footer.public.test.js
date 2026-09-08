var JSONStream = require('../');
var it = require('it-is');

exports['header and footer parse'] = function (test) {
  var input = '{"start":"alpha"}[{"one":1},{"two":2}]{"end":"omega"}';
  var parser = JSONStream.parse('*');
  var results = [];

  parser.on('data', function (obj) {
    results.push(obj);
  });
  parser.on('end', function () {
    it(results).deepEqual([{one: 1}, {two: 2}]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(input);
  parser.end();
};