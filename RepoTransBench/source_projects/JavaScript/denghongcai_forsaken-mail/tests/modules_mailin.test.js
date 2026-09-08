jest.mock('mailin', () => {
  let handlers = {};
  return {
    start: jest.fn(),
    on: jest.fn((event, cb) => {
      handlers[event] = cb;
    }),
    _handlers: handlers,
  };
});

describe('modules/mailin.js', () => {
  beforeEach(() => {
    jest.resetModules();
  });

  test('calls mailin.start and error handler logs on error', () => {
    global.console = { error: jest.fn() };
    const mailin = require('../modules/mailin');
    expect(mailin.start).toHaveBeenCalled();
    // Simulate error
    mailin.on.mock.calls.find(c => c[0] === 'error')[1](new Error('fail!'));
    expect(console.error).toHaveBeenCalledWith(expect.stringMatching(/fail/));
  });
});