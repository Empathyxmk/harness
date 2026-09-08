var JSONStream = require('../');
var it = require('it-is');

exports['error contains json snippet'] = function (test) {
  var parser = JSONStream.parse();
  var receivedError = false;
  parser.on('error', function (err) {
    receivedError = true;
    it(err.message).match(/Unexpected token/);
    it(err.message).match(/"wrong"/);
    if (test && typeof test.done === 'function') test.done();
  });
  parser.write('{ "wrong": }');
  parser.end();
};

exports['error contains partial input'] = function (test) {
  var parser = JSONStream.parse();
  var errors = [];
  parser.on('error', function (err) {
    errors.push(err);
  });
  parser.write('{ "foo": ');
  parser.end();
  it(errors.length).equal(1);
  it(errors[0].message).ok();
};