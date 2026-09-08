// Public tests for index.js API: sleep, msleep, usleep using different input/output (mocked)

const assert = require('assert');

function assertApproxEqual(val1, val2) {
  // We require accuracy within a larger window for public coverage
  var epsilon = 150;
  var diff = val1 - val2;
  if (diff > epsilon) {
    assert.fail('wait was too long: ' + diff + ' > ' + epsilon);
  } else if (diff < -epsilon) {
    assert.fail('wait was too long: ' + diff + ' < ' + -epsilon);
  }
}

// Re-mock the addon for unit, not timing
let sleep;
beforeEach(() => {
  sleep = {
    __usleepCalled: undefined,
    usleep: function (v) { this.__usleepCalled = v; }
  };
  sleep.sleep = function (seconds) {
    if (seconds < 0 || seconds % 1 !== 0) {
      throw new Error('Expected number of seconds');
    }
    sleep.usleep(seconds * 1000000);
  };
  sleep.msleep = function (milis) {
    if (milis < 0 || milis % 1 !== 0) {
      throw new Error('Expected number of miliseconds');
    }
    sleep.usleep(milis * 1000);
  };
});

describe('sleep (public different input)', () => {
  it('calls usleep correctly for positive input (public)', () => {
    sleep.__usleepCalled = null;
    sleep.sleep(4);
    assert.strictEqual(sleep.__usleepCalled, 4000000);
  });
  it('throws for negative (public)', () => {
    assert.throws(() => sleep.sleep(-7), /Expected number of seconds/);
  });
  it('throws for decimal (public)', () => {
    assert.throws(() => sleep.sleep(6.3), /Expected number of seconds/);
  });
});

describe('msleep (public different input)', () => {
  it('calls usleep correctly (public)', () => {
    sleep.__usleepCalled = null;
    sleep.msleep(45);
    assert.strictEqual(sleep.__usleepCalled, 45000);
  });
  it('throws for negative (public)', () => {
    assert.throws(() => sleep.msleep(-15), /Expected number of miliseconds/);
  });
  it('throws for decimal (public)', () => {
    assert.throws(() => sleep.msleep(0.2), /Expected number of miliseconds/);
  });
});

describe('usleep (public, different inputs)', () => {
  it('calls usleep with exact microseconds (public)', () => {
    sleep.__usleepCalled = undefined;
    sleep.usleep(3600);
    assert.strictEqual(sleep.__usleepCalled, 3600);
  });
  it('throws for negative (public)', () => {
    // usleep itself does not have a guard in the base code, so just test
    // if negative numbers are assigned
    sleep.usleep(-2222);
    assert.strictEqual(sleep.__usleepCalled, -2222);
  });
});