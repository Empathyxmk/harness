const yargs = {
  commandDir: jest.fn().mockReturnThis(),
  recommendCommands: jest.fn().mockReturnThis(),
  demandCommand: jest.fn().mockReturnThis(),
  argv: {}
}
module.exports = yargs;