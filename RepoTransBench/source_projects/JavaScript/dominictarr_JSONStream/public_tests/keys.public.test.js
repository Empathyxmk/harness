var JSONStream = require('../');
var it = require('it-is');

exports['extract top-level keys from a different object'] = function (test) {
  var parser = JSONStream.keys;
  var stream = parser ? parser('users') : JSONStream.parse('users.*');

  var results = [];
  var obj = { users: { alice: 11, bob: 22, charlie: 33 } };

  stream.on('data', function (val) { results.push(val); });
  stream.on('end', function () {
    it(results).deepEqual([11, 22, 33]);
    if (test && typeof test.done === 'function') test.done();
  });

  stream.write(JSON.stringify(obj));
  stream.end();
};

exports['array path extraction with different values'] = function (test) {
  var parser = JSONStream.parse(['team', true]);
  var results = [];
  var obj = { team: [{ member: 100 }, { member: 200 }, { member: 300 }] };

  parser.on('data', function (val) {
    results.push(val);
  });
  parser.on('end', function () {
    it(results).deepEqual([{ member: 100 }, { member: 200 }, { member: 300 }]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(JSON.stringify(obj));
  parser.end();
};

exports['advanced keys with more levels'] = function (test) {
  var parser = JSONStream.parse(['company', 'departments', true, 'people', true, 'name']);
  var results = [];
  var obj = { company: { departments: [
    { people: [{ name: "Jane" }, { name: "John" }] },
    { people: [{ name: "Alice" }] }
  ] } };

  parser.on('data', function (val) {
    results.push(val);
  });
  parser.on('end', function () {
    it(results).deepEqual(["Jane", "John", "Alice"]);
    if (test && typeof test.done === 'function') test.done();
  });

  parser.write(JSON.stringify(obj));
  parser.end();
};