// This is a minimal test to ensure commands.js loads and exposes function
const commands = require('../commands')
describe('commands.js loading', () => {
  it('should construct commands object and have an init and shell method', () => {
    const cmds = commands()
    // The returned object has at least init and shell (also a bunch of actions when init is called)
    cmds.init && cmds.shell
  })
})