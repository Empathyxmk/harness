/**
 * Test src/ch01/listing1_7/listing1_7.js, mocking Rx.Observable
 */
describe('ch01/listing1_7/listing1_7.js', () => {
  let origConsoleLog;
  let origRx;

  beforeEach(() => {
    origConsoleLog = global.console.log;
    global.console.log = jest.fn();
    // Mock Rx.Observable with chainable methods
    const subscribe = jest.fn(cb => {
      cb('111-22-3333');
    });
    const filter = jest.fn(() => ({ subscribe }));
    const map = jest.fn(() => ({ filter, subscribe }));
    const pluck = jest.fn(() => ({ map, filter, subscribe }));
    const fromEvent = jest.fn(() => ({ pluck, map, filter, subscribe }));
    global.Rx = {
      Observable: { fromEvent }
    };
    // document.querySelector mock for student-ssn
    global.document = { querySelector: jest.fn(() => ({})) };
  });

  afterEach(() => {
    global.console.log = origConsoleLog;
    delete global.Rx;
    delete global.document;
  });

  it('should log Valid SSN when a valid input passes', () => {
    require('../listing1_7/listing1_7.js');
    expect(console.log).toHaveBeenCalledWith('Valid SSN 111-22-3333');
  });
});