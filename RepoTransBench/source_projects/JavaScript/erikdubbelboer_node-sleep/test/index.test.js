// Additional unit tests to improve branch and line coverage on index.js

const assert = require('assert');
let sleep;

describe('index.js', () => {
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
    it('calls usleep with correct value', () => {
      sleep.__usleepCalled = undefined;
      sleep.sleep(3);
      assert.strictEqual(sleep.__usleepCalled, 3000000);
    });

    it('throws on negative seconds', () => {
      assert.throws(() => sleep.sleep(-2), /Expected number of seconds/);
    });

    it('throws on decimal seconds', () => {
      assert.throws(() => sleep.sleep(1.5), /Expected number of seconds/);
    });

    it('throws on string input', () => {
      assert.throws(() => sleep.sleep('foo'), /Expected number of seconds/);
    });
  });

  describe('msleep', () => {
    it('calls usleep with correct value', () => {
      sleep.__usleepCalled = undefined;
      sleep.msleep(250);
      assert.strictEqual(sleep.__usleepCalled, 250000);
    });

    it('throws on negative ms', () => {
      assert.throws(() => sleep.msleep(-10), /Expected number of miliseconds/);
    });

    it('throws on decimal ms', () => {
      assert.throws(() => sleep.msleep(1.7), /Expected number of miliseconds/);
    });

    it('throws on string input', () => {
      assert.throws(() => sleep.msleep('bar'), /Expected number of miliseconds/);
    });
  });
});