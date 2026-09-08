jest.mock('yargs', () => ({
  commandDir: jest.fn().mockReturnThis(),
  recommendCommands: jest.fn().mockReturnThis(),
  demandCommand: jest.fn().mockReturnThis(),
  argv: {}
}));
const yargs = require('yargs');
const path = require('path');

describe('cli/index', () => {
  it('runs yargs with proper API', () => {
    require('./index');
    expect(yargs.commandDir).toBeCalledWith(path.join(__dirname, 'commands'));
    expect(yargs.recommendCommands).toBeCalled();
    expect(yargs.demandCommand).toBeCalled();
  });
});