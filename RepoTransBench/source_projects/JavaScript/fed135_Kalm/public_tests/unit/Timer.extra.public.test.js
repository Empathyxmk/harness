const Timer = require('../../src/Timer');
const { expect } = require('chai');

describe('Timer - Public Edge Cases', () => {
  it('should clear interval on stop() [diff value]', () => {
    const timer = new Timer(15);
    expect(timer.timer).to.not.be.null;
    timer.stop();
    expect(timer.timer).to.be.null;
  });

  it('should restart timer with start(), different delay', (done) => {
    const timer = new Timer(8);
    timer.stop();
    expect(timer.timer).to.be.null;
    timer.start();
    setTimeout(() => {
      expect(timer.timer).to.not.be.null;
      timer.stop();
      done();
    }, 15);
  });

  it('should emit step multiple times', (done) => {
    const timer = new Timer(3);
    let callCount = 0;
    const maxCalls = 2;
    timer.on('step', () => {
      callCount++;
      if (callCount >= maxCalls) {
        timer.stop();
        expect(callCount).to.equal(maxCalls);
        done();
      }
    });
  });
});