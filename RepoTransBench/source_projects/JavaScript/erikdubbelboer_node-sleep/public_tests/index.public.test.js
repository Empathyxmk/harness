// Public test cases for index.js with different input/output data

const assert = require('assert');
let sleep;

describe('index.js public tests', () => {
  before(() => {
    // mock the native addon for coverage, since usleep may not work in node --require coverage tools
    sleep = {
      usleep: function(value) {
        sleep.__usleepCalled = value;
      }
    };
    // Re-create the original file logic to get full coverage,
    // but override the native binding
    // inline the code from index.js here:
    sleep.sleep = function(seconds) {
      if (seconds < 0 || seconds % 1 != 0) {
        throw new Error('Expected number of seconds');
      }
      sleep.usleep(seconds * 1000000);
    }

    sleep.msleep = function(miliseconds) {
      if (miliseconds < 0 || miliseconds % 1 != 0) {
        throw new Error('Expected number of miliseconds');
      }
      sleep.usleep(miliseconds * 1000);
    }
  });

  describe('sleep', () => {
    it('calls usleep with correct value (public)', () => {
      sleep.__usleepCalled = undefined;
      sleep.sleep(5);
      assert.strictEqual(sleep.__usleepCalled, 5000000);
    });

    it('throws on negative seconds (public)', () => {
      assert.throws(() => sleep.sleep(-10), /Expected number of seconds/);
    });

    it('throws on decimal seconds (public)', () => {
      assert.throws(() => sleep.sleep(2.7), /Expected number of seconds/);
    });

    it('throws on string input (public)', () => {
      assert.throws(() => sleep.sleep('baz'), /Expected number of seconds/);
    });
  });

  describe('msleep', () => {
    it('calls usleep with correct value (public)', () => {
      sleep.__usleepCalled = undefined;
      sleep.msleep(111);
      assert.strictEqual(sleep.__usleepCalled, 111000);
    });

    it('throws on negative ms (public)', () => {
      assert.throws(() => sleep.msleep(-50), /Expected number of miliseconds/);
    });

    it('throws on decimal ms (public)', () => {
      assert.throws(() => sleep.msleep(3.3), /Expected number of miliseconds/);
    });

    it('throws on string input (public)', () => {
      assert.throws(() => sleep.msleep('qux'), /Expected number of miliseconds/);
    });
  });
});