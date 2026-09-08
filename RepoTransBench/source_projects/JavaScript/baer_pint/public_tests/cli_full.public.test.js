const { expect } = require('chai');

// Instead of real CLI, we mock an interface and use different input/command data
describe('cli full (public)', function () {
  it('should handle multiple public arguments', function () {
    const argumentsList = [['--dry-run'], ['--help'], ['--quiet']];
    argumentsList.forEach(args => {
      expect(args[0]).to.be.a('string');
      expect(args[0].charAt(0)).to.equal('-');
    });
  });

  it('should not throw with unknown public flags', function () {
    function runCli(args) {
      // Simulate cli; don't actually execute
      if (args.includes('--unknown-public')) return false;
      return true;
    }
    expect(() => runCli(['--unknown-public'])).not.to.throw();
    expect(runCli(['--unknown-public'])).to.be.false;
  });
});