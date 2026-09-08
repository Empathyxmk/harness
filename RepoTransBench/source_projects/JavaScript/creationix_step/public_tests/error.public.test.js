require('./helper');

// Use a different error/message
var pubException = new Error('Catch public!');

expect('first');
expect('wait_public');
expect('second');
expect('third');
Step(
  function () {
    fulfill('first');
    var callback = this;
    setTimeout(function () {
      fulfill('wait_public');
      callback(pubException);
    }, 0);
  },
  function (err) {
    fulfill('second');
    assert.equal(pubException, err, "public error should be passed through");
    throw pubException;
  },
  function (err) {
    fulfill('third');
    assert.equal(pubException, err, "public error should be caught");
  }
);