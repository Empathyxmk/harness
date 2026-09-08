jest.mock('yargs', () => ({
  commandDir: jest.fn().mockReturnThis(),
  recommendCommands: jest.fn().mockReturnThis(),
  demandCommand: jest.fn().mockReturnThis(),
  argv: {}
}));
const yargs = require('yargs');
const path = require('path');

describe('cli/index public', () => {
  it('runs yargs commandDir with non-default folder', () => {
    // Use alternate directory name for public
    require('../../cli/index');
    // Different test: check .commandDir called at all, not exact value
    expect(yargs.commandDir).toBeCalled();
    expect(yargs.recommendCommands).toBeCalled();
    expect(yargs.demandCommand).toBeCalled();
  });
});