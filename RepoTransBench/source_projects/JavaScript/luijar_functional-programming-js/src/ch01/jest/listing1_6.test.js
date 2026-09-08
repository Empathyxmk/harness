/**
 * Test src/ch01/listing1_6/listing1_6.js (DOM interactions polyfilled)
 */
describe('ch01/listing1_6/listing1_6.js', () => {
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

  it('should log valid ssn and set valid=true for correct input', () => {
    require('../listing1_6/listing1_6.js');
    // simulate user input
    elem.value = '123-45-6789';
    elem.onkeyup({}); // triggers the handler
    expect(console.log).toHaveBeenCalledWith('Valid SSN: 123456789!');
  });

  it('should log invalid ssn for empty input', () => {
    require('../listing1_6/listing1_6.js');
    elem.value = '';
    elem.onkeyup({});
    expect(console.log).toHaveBeenCalledWith('Invalid SSN: !');
  });

  it('should do nothing for incomplete ssn', () => {
    require('../listing1_6/listing1_6.js');
    elem.value = '12';
    elem.onkeyup({});
    expect(console.log).not.toHaveBeenCalledWith(expect.stringContaining('Valid SSN'));
    // Should not log valid
  });
});