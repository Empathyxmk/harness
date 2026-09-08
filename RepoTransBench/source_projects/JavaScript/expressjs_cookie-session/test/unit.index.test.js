// Minimal Jest-compatible test for index.js
const cookieSession = require('../index');

describe('index.js', () => {
  it('exports a function', () => {
    expect(typeof cookieSession).toBe('function')
  })
})