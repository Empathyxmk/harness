var JSONStream = require('../');
var it = require('it-is');
var Stream = require('stream');

// Test: stringify array of numbers with custom open/close/sep
exports['stringify array of numbers with custom sep'] = function (test) {
  var stringifyStream = JSONStream.stringify('[', ']', ';');
  var input = [100, 200, 300];
  var result = '';
  stringifyStream.on('data', function (chunk) {
    result += chunk;
  });
  stringifyStream.on('end', function () {
    it(result).equal('[100;200;300]');
    if (test && typeof test.done === 'function') test.done();
  });

  input.forEach(function (x) {
    stringifyStream.write(x);
  });
  stringifyStream.end();
};

// Test: stringify array of objects with different properties
exports['stringify array of objects with alternative data'] = function (test) {
  var stringifyStream = JSONStream.stringify('[', ']', ',');
  var input = [
    {id: 5, pet: "Dog"},
    {id: 3, pet: "Cat"},
    {id: 15, pet: "Rabbit"}
  ];
  var result = '';
  stringifyStream.on('data', function (chunk) {
    result += chunk;
  });
  stringifyStream.on('end', function () {
    it(JSON.parse(result)).deepEqual(input);
    if (test && typeof test.done === 'function') test.done();
  });

  input.forEach(function (obj) {
    stringifyStream.write(obj);
  });
  stringifyStream.end();
};

// Test: stringify single value (string)
exports['stringify single string value with custom delim'] = function(test) {
  var stringifyStream = JSONStream.stringify('||', '||', '-');
  var result = '';
  stringifyStream.on('data', function(chunk) {
    result += chunk;
  });
  stringifyStream.on('end', function() {
    it(result).equal('||"hello"||');
    if (test && typeof test.done === 'function') test.done();
  });
  stringifyStream.write("hello");
  stringifyStream.end();
};