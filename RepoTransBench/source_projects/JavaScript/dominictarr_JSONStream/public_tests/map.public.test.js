var JSONStream = require('../');
var it = require('it-is');

exports['map function with alternative mapping and data'] = function (test) {
  var parser = JSONStream.parse('collection.*', function (item) {
    return item && item.n ? item.n * 10 : item;
  });

  var results = [];
  var input = { collection: [{ n: 4 }, { n: 5 }, { n: 6 }] };

  parser.on('data', function (val) {
    results.push(val);
  });
  parser.on('end', function () {
    it(results).deepEqual([40, 50, 60]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(JSON.stringify(input));
  parser.end();
};

exports['map with missing n property and alternative data'] = function (test) {
  var parser = JSONStream.parse('collectionTwo.*', function (item) {
    return item && item.n ? item.n * 2 : 0;
  });

  var results = [];
  var input = { collectionTwo: [{ n: 9 }, {}, { n: 12 }] };

  parser.on('data', function (val) {
    results.push(val);
  });
  parser.on('end', function () {
    it(results).deepEqual([18, 0, 24]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(JSON.stringify(input));
  parser.end();
};

exports['map with string property extraction'] = function (test) {
  var parser = JSONStream.parse('users.*', function (item) {
    return item && item.name ? item.name : null;
  });

  var results = [];
  var input = { users: [{ name: "Jerry" }, { name: "Elaine" }, { notName: true }] };

  parser.on('data', function (val) {
    results.push(val);
  });
  parser.on('end', function () {
    it(results).deepEqual(["Jerry", "Elaine", null]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(JSON.stringify(input));
  parser.end();
};