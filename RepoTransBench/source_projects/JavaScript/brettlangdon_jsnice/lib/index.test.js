const http = require('http');
const { nicify } = require('./index');

jest.mock('http');

describe('nicify', () => {
  let writeMock, endMock;

  beforeEach(() => {
    writeMock = jest.fn();
    endMock = jest.fn();

    // Default http.request mock: simulate working POST with data, then end
    http.request.mockImplementation((options, cb) => {
      // Fake 'res' with chained 'on' methods for 'data' and 'end'
      const res = {
        on: jest.fn((event, handler) => {
          if (event === 'data') {
            setImmediate(() => handler('{"result":"beautified"}'));
          }
          if (event === 'end') {
            setImmediate(() => handler());
          }
        }),
      };
      setImmediate(() => cb(res));
      return {
        on: jest.fn(),
        write: writeMock,
        end: endMock,
      };
    });
  });

  afterEach(() => {
    jest.resetAllMocks();
  });

  it('calls callback with parsed data and default options', done => {
    nicify('let x=1;', (err, data) => {
      expect(err).toBeNull();
      expect(data).toEqual({ result: "beautified" });
      expect(writeMock).toHaveBeenCalledWith('let x=1;');
      expect(endMock).toHaveBeenCalled();
      done();
    });
  });

  it('handles all options branches', done => {
    // All set false/true to exercise different branches
    nicify('let x=2;', { pretty: false, rename: true, types: false, suggest: true }, (err, data) => {
      expect(err).toBeNull();
      expect(data).toEqual({ result: "beautified" });
      expect(writeMock).toHaveBeenCalledWith('let x=2;');
      expect(endMock).toHaveBeenCalled();
      done();
    });
  });

  it('treats options as optional (callback as second arg)', done => {
    nicify('let y=3;', done);
  });

  it('calls callback on http.request error', done => {
    // this mock emits only error event
    http.request.mockImplementation(() => ({
      on: (evt, fn) => { if (evt === 'error') setImmediate(() => fn(new Error('request fail'))); },
      write: writeMock,
      end: endMock,
    }));

    nicify('let err=0;', (err, result) => {
      expect(err).toBeInstanceOf(Error);
      expect(result).toBeNull();
      done();
    });
  });

  it('calls callback if JSON.parse throws', done => {
    http.request.mockImplementation((options, cb) => {
      const res = {
        on: jest.fn((event, handler) => {
          // send invalid JSON
          if (event === 'data') setImmediate(() => handler('oops not-json'));
          if (event === 'end') setImmediate(() => handler());
        }),
      };
      setImmediate(() => cb(res));
      return {
        on: jest.fn(),
        write: writeMock,
        end: endMock,
      };
    });

    // Patch module to catch thrown error in callback
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
    let errorHandled = false;

    nicify('let bad=5;', (err, result) => {
      // test catches thrown error and handles undefined result
      expect(err).toBeTruthy();
      expect(result).toBeUndefined();
      errorHandled = true;
      consoleError.mockRestore();
      done();
    });
  });

  it('should set all options to default when not provided', done => {
    // Omit options completely, force default branch for each
    http.request.mockImplementation((options, cb) => {
      expect(options.path).toMatch(/\bpretty=1\b/);
      expect(options.path).toMatch(/\brename=1\b/);
      expect(options.path).toMatch(/\btypes=1\b/);
      expect(options.path).toMatch(/\bsuggest=0\b/);
      const res = {
        on: jest.fn((event, handler) => {
          if (event === 'data') setImmediate(() => handler('{"foo":"bar"}'));
          if (event === 'end') setImmediate(() => handler());
        }),
      };
      setImmediate(() => cb(res));
      return {
        on: jest.fn(),
        write: writeMock,
        end: endMock,
      };
    });

    nicify('let q=9;', (err, data) => {
      expect(data).toEqual({ foo: "bar" });
      done();
    });
  });
});