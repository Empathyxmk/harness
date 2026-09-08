const http = require('http');
const { nicify } = require('../../lib/index');

jest.mock('http');

describe('nicify (public test cases)', () => {
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
            setImmediate(() => handler('{"otherResult":"formatted"}'));
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

  it('calls callback with parsed data and default options (public)', done => {
    nicify('const z=99;', (err, data) => {
      expect(err).toBeNull();
      expect(data).toEqual({ otherResult: "formatted" });
      expect(writeMock).toHaveBeenCalledWith('const z=99;');
      expect(endMock).toHaveBeenCalled();
      done();
    });
  });

  it('handles all options branches with public test data', done => {
    // Different values for code/options
    nicify(
      'function go(a){return a+1;}', 
      { pretty: true, rename: false, types: true, suggest: false },
      (err, data) => {
        expect(err).toBeNull();
        expect(data).toEqual({ otherResult: "formatted" });
        expect(writeMock).toHaveBeenCalledWith('function go(a){return a+1;}');
        expect(endMock).toHaveBeenCalled();
        done();
      }
    );
  });

  it('treats options as optional with public test code', done => {
    nicify('var w=42;', done);
  });

  it('calls callback on http.request error (public variant)', done => {
    // this mock emits only error event for public test case
    http.request.mockImplementation(() => ({
      on: (evt, fn) => { if (evt === 'error') setImmediate(() => fn(new Error('connection fail'))); },
      write: writeMock,
      end: endMock,
    }));

    nicify('const fail=true;', (err, result) => {
      expect(err).toBeInstanceOf(Error);
      expect(result).toBeNull();
      done();
    });
  });

  it('calls callback if JSON.parse throws (public case)', done => {
    http.request.mockImplementation((options, cb) => {
      const res = {
        on: jest.fn((event, handler) => {
          // send invalid JSON
          if (event === 'data') setImmediate(() => handler('invalid:json'));
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

    nicify('for(let j=0;j<5;j++){}', (err, result) => {
      expect(err).toBeTruthy();
      expect(result).toBeUndefined();
      errorHandled = true;
      consoleError.mockRestore();
      done();
    });
  });

  it('should set all options to default when not provided (public test)', done => {
    // Omit options, test parsing expected path with all default options
    http.request.mockImplementation((options, cb) => {
      expect(options.path).toMatch(/\bpretty=1\b/);
      expect(options.path).toMatch(/\brename=1\b/);
      expect(options.path).toMatch(/\btypes=1\b/);
      expect(options.path).toMatch(/\bsuggest=0\b/);
      const res = {
        on: jest.fn((event, handler) => {
          if (event === 'data') setImmediate(() => handler('{"baz":"quux"}'));
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

    nicify('var t=77;', (err, data) => {
      expect(data).toEqual({ baz: "quux" });
      done();
    });
  });
});