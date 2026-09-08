// Mock for 'cordova' for use in jest environment

module.exports = {
  exec: jest.fn(),
  argscheck: {
    checkArgs: jest.fn()
  }
};