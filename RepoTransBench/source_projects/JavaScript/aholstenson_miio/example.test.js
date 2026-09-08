// Improved version for handling asynchronous console error after failed device connection

afterEach(() => {
  jest.resetModules();
  jest.clearAllMocks();
});

describe('example code', () => {
  it('should connect to device successfully', (done) => {
    jest.resetModules();
    jest.doMock('./lib', () => ({
      device: jest.fn(({ address }) => {
        if (address === 'ipHere') return Promise.resolve({ id: 'abc' });
        return Promise.reject(new Error('bad address'));
      }),
    }));
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    require('./example.js'); // Should eventually call device()
    setTimeout(() => {
      expect(require('./lib').device).toBeCalledWith({ address: 'ipHere' });
      spy.mockRestore();
      done();
    }, 50);
  });

  it('should print error if device connection fails', (done) => {
    jest.resetModules();
    jest.doMock('./lib', () => ({
      device: jest.fn(() => Promise.reject(new Error('fail')))
    }));
    const spy = jest.spyOn(console, "log").mockImplementation(() => {});
    const origExit = process.exit;
    process.exit = () => {};
    require('./example.js');
    // Listen for up to 100ms for error logging to show up
    let waited = 0;
    function check() {
      if (
        spy.mock.calls.some(
          call => call[0] && call[0].toString().includes('Error occurred')
        )
      ) {
        spy.mockRestore();
        process.exit = origExit;
        done();
      } else if (waited >= 100) {
        spy.mockRestore();
        process.exit = origExit;
        // Show the error message for debugging purposes
        // console.log('mock.calls:', spy.mock.calls);
        done.fail(new Error('Did not log error as expected'));
      } else {
        waited += 10;
        setTimeout(check, 10);
      }
    }
    setTimeout(check, 10);
  }, 200);
});