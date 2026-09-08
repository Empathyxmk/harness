// helpers.js - exposes the testJson helper for tests
const Stream = require('stream').Writable;

module.exports = {
  testJson: function (opts, writable, cb) {
    // Simulate JSON streaming for tests
    const array = [{ test: "object1" }, { test: "object2" }];
    if (opts && opts.streamArray) {
      writable.write('[\n');
      writable.write(JSON.stringify(array[0]));
      writable.write(',\n');
      writable.write(JSON.stringify(array[1]));
      writable.write('\n]\n');
      writable.end();
    } else {
      writable.write(JSON.stringify(array));
      writable.end();
    }
    writable.on('finish', cb);
  }
};