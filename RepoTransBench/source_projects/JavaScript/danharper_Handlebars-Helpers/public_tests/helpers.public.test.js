const Handlebars = require('handlebars');
const ExpressionRegistry = require('../src/helpers');

describe('ExpressionRegistry (public)', () => {
  it('should compare not operator with different values', () => {
    expect(ExpressionRegistry.call('not', 'x', 'y')).toBe(true);
    expect(ExpressionRegistry.call('not', 'z', 'z')).toBe(false);
  });

  it('should compare > operator with other numbers', () => {
    expect(ExpressionRegistry.call('>', 10, 5)).toBe(true);
    expect(ExpressionRegistry.call('>', -1, 0)).toBe(false);
  });

  it('should compare < operator with different numbers', () => {
    expect(ExpressionRegistry.call('<', 3, 10)).toBe(true);
    expect(ExpressionRegistry.call('<', 5, 2)).toBe(false);
  });

  it('should compare >= operator with different numbers', () => {
    expect(ExpressionRegistry.call('>=', 42, 41)).toBe(true);
    expect(ExpressionRegistry.call('>=', 99, 100)).toBe(false);
  });

  it('should compare <= operator with different numbers', () => {
    expect(ExpressionRegistry.call('<=', 17, 23)).toBe(true);
    expect(ExpressionRegistry.call('<=', 30, 20)).toBe(false);
  });

  it('should compare === operator with different type/values', () => {
    expect(ExpressionRegistry.call('===', 'test', 'test')).toBe(true);
    expect(ExpressionRegistry.call('===', '100', 100)).toBe(false);
  });

  it('should compare !== operator with different values and types', () => {
    expect(ExpressionRegistry.call('!==', false, 0)).toBe(true);
    expect(ExpressionRegistry.call('!==', 3.14, 3.14)).toBe(false);
  });

  it('should compare in operator with array different values', () => {
    expect(ExpressionRegistry.call('in', 'apple', ['pear', 'apple', 'banana'])).toBe(true);
    expect(ExpressionRegistry.call('in', 'kiwi', ['pear', 'apple', 'banana'])).toBe(false);
  });

  it('should compare in operator with comma string (public)', () => {
    expect(ExpressionRegistry.call('in', 'red', 'red,blue,green')).toBe(true);
    expect(ExpressionRegistry.call('in', 'yellow', 'red,blue,green')).toBe(false);
  });

  it('should throw on unknown operator (public)', () => {
    expect(() => {
      ExpressionRegistry.call('unknown_operator', 5, 10);
    }).toThrow('Unknown operator "unknown_operator"');
  });
});

describe('is helper (public)', () => {
  let template, context, outTrue, outFalse;
  beforeEach(() => {
    outTrue = 'PASS';
    outFalse = 'FAIL';
  });

  it('should support boolean context with false/true (public)', () => {
    template = Handlebars.compile('{{#is active}}PASS{{else}}FAIL{{/is}}');
    context = { active: false };
    expect(template(context)).toBe('FAIL');
    context = { active: 123 }; // truthy
    expect(template(context)).toBe('PASS');
  });

  it('should support equality (args length 3) with different data (public)', () => {
    template = Handlebars.compile('{{#is foo bar}}PASS{{else}}FAIL{{/is}}');
    context = { foo: 'x', bar: 'x' };
    expect(template(context)).toBe('PASS');
    context = { foo: 'x', bar: 'y' };
    expect(template(context)).toBe('FAIL');
  });

  it('should support operator form (args length > 3) with < and other numbers (public)', () => {
    template = Handlebars.compile('{{#is score "<" max}}PASS{{else}}FAIL{{/is}}');
    context = { score: 4, max: 10 };
    expect(template(context)).toBe('PASS');
    context = { score: 11, max: 10 };
    expect(template(context)).toBe('FAIL');
  });

  it('should support "in" operator with alternative list (public)', () => {
    template = Handlebars.compile('{{#is color "in" palette}}PASS{{else}}FAIL{{/is}}');
    context = { color: 'blue', palette: ['red', 'blue'] };
    expect(template(context)).toBe('PASS');
    context = { color: 'green', palette: ['red', 'blue'] };
    expect(template(context)).toBe('FAIL');
  });
});

describe('nl2br helper (public)', () => {
  it('should convert newlines to <br> with other input', () => {
    const template = Handlebars.compile('{{nl2br text}}');
    const result = template({ text: 'alpha\r\nbeta\ngamma' });
    expect(result).toMatch(/alpha<br>(\n|\r\n)beta<br>(\n|\r\n)gamma/);
  });

  it('should handle undefined and numeric zero values', () => {
    const template = Handlebars.compile('{{nl2br text}}');
    expect(template({ text: undefined })).toBe('undefined');
    expect(template({ text: 0 })).toBe('0');
  });
});

describe('log helper (public)', () => {
  it('calls console.log with different values', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const template = Handlebars.compile('{{log "message" 42}}');
    template({});
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
});

describe('debug helper (public)', () => {
  it('calls console.log with other context and values', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const data = { animal: 'dog' };
    const template = Handlebars.compile('{{debug true animal}}');
    template(data);
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
});