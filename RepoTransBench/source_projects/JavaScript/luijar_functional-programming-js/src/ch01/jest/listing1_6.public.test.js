/**
 * Public Test src/ch01/listing1_6/listing1_6.js (DOM interactions polyfilled with new test data)
 */
describe('ch01/listing1_6/listing1_6.js (public test)', () => {
  let originalConsoleLog;
  let elem;

  beforeAll(() => {
    if (!global.document) {
      global.document = {};
    }
    global.document.querySelector = jest.fn(() => ({
      value: '',
      onkeyup: null
    }));
  });

  beforeEach(() => {
    elem = { value: '', onkeyup: null };
    global.document.querySelector.mockReturnValue(elem);
    originalConsoleLog = global.console.log;
    global.console.log = jest.fn();
    jest.resetModules();
  });

  afterEach(() => {
    global.console.log = originalConsoleLog;
  });

  it('should log valid ssn and set valid=true for another correct input', () => {
    require('../listing1_6/listing1_6.js');
    // simulate different user input
    elem.value = '987-65-4321';
    elem.onkeyup({});
    expect(console.log).toHaveBeenCalledWith('Valid SSN: 987654321!');
  });

  it('should log invalid ssn for a different empty input', () => {
    require('../listing1_6/listing1_6.js');
    elem.value = '';
    elem.onkeyup({});
    expect(console.log).toHaveBeenCalledWith('Invalid SSN: !');
  });

  it('should do nothing for another incomplete ssn', () => {
    require('../listing1_6/listing1_6.js');
    elem.value = '9-8';
    elem.onkeyup({});
    expect(console.log).not.toHaveBeenCalledWith(expect.stringContaining('Valid SSN'));
    // Should not log valid
  });
});