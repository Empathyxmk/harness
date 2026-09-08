// Integration-like (timing) public tests with different sleep values (use less common numbers)

const assert = require('assert');
const child_process = require('child_process');

let sleep;
try {
  sleep = require('../');
} catch (e) {
  // Native not built - skip timing test gracefully
  sleep = null;
}

function assertApproxEqual(val1, val2) {
  var epsilon = 150;
  var diff = val1 - val2;
  if (diff > epsilon) {
    assert.fail('wait was too long: ' + diff + ' > ' + epsilon);
  } else if (diff < -epsilon) {
    assert.fail('wait was too long: ' + diff + ' < ' + -epsilon);
  }
}

(sleep ? describe : describe.skip)('Public/Integration sleep API', function () {
  it('sleep works for new input', function () {
    var sleepTime = 2;
    var start = new Date();
    sleep.sleep(sleepTime);
    var end = new Date();
    assertApproxEqual(end - start, sleepTime * 1000);
  });

  it('sleep works for one (public)', function () {
    var sleepTime = 1;
    var start = new Date();
    sleep.sleep(sleepTime);
    var end = new Date();
    assertApproxEqual(end - start, sleepTime * 1000);
  });

  it('sleep does not allow negative numbers (public)', function () {
    assert.throws(function () {
      sleep.sleep(-8);
    });
  });

  it('works with child_process (public)', function () {
    var sleepTime = 2;
    child_process.exec('echo hello', function (err, stdout, stderr) { });
    var start = new Date();
    sleep.sleep(sleepTime);
    var end = new Date();
    assertApproxEqual(end - start, sleepTime * 1000);
  });

  it('usleep works for a typical microsecond value (public)', function () {
    var sleepTime = 100000;
    var start = new Date();
    sleep.usleep(sleepTime);
    var end = new Date();
    assertApproxEqual(end - start, sleepTime / 1000);
  });

  it('usleep works for a large microsecond value (public)', function () {
    this.timeout(5000);
    var sleepTime = 1500000;
    var start = new Date();
    sleep.usleep(sleepTime);
    var end = new Date();
    assertApproxEqual(end - start, sleepTime / 1000);
  });

  it('usleep does not allow negative (public)', function () {
    assert.throws(function () {
      sleep.usleep(-111);
    });
  });

  it('msleep works for new normal input (public)', function() {
    var sleepTime = 6;
    var start = new Date();
    sleep.msleep(sleepTime);
    var end = new Date();
    assertApproxEqual(end - start, sleepTime);
  });

  it('msleep does not allow negative (public)', function () {
    assert.throws(function () {
      sleep.msleep(-13);
    });
  });

  it('msleep does not allow decimal (public)', function () {
    assert.throws(function () {
      sleep.msleep(5.7);
    });
  });
});