const Timer = require('../../src/Timer');
const { expect } = require('chai');

describe('Timer - Edge Cases', () => {
  it('should clear interval on stop()', () => {
    const timer = new Timer(10);
    expect(timer.timer).to.not.be.null;
    timer.stop();
    expect(timer.timer).to.be.null;
  });

  it('should restart timer with start()', (done) => {
    const timer = new Timer(5);
    timer.stop();
    expect(timer.timer).to.be.null;
    timer.start();
    setTimeout(() => {
      expect(timer.timer).to.not.be.null;
      timer.stop();
      done();
    }, 10);
  });

  it('should emit step on timer tick', (done) => {
    const timer = new Timer(2);
    let called = false;
    timer.on('step', () => {
      called = true;
      timer.stop();
      expect(called).to.be.true;
      done();
    });
  });
});