const protocol = require('./protocol');
const path = require('path');

describe('cli/commands/protocol', () => {
  it('should expose correct properties and call handler', () => {
    expect(protocol.command).toBe('protocol <command>');
    expect(protocol.description).toBeDefined();
    // builder returns a value with .commandDir method
    const yargs = { commandDir: jest.fn().mockReturnValue(42) };
    expect(protocol.builder(yargs)).toBe(42);
    expect(protocol.handler()).toBeUndefined();
  });
});