const Handlebars = require('handlebars');
const ExpressionRegistry = require('../src/helpers');

describe('ExpressionRegistry', () => {
  it('should compare not operator', () => {
    expect(ExpressionRegistry.call('not', 1, 2)).toBe(true);
    expect(ExpressionRegistry.call('not', 2, 2)).toBe(false);
  });

  it('should compare > operator', () => {
    expect(ExpressionRegistry.call('>', 3, 2)).toBe(true);
    expect(ExpressionRegistry.call('>', 1, 2)).toBe(false);
  });

  it('should compare < operator', () => {
    expect(ExpressionRegistry.call('<', 1, 2)).toBe(true);
    expect(ExpressionRegistry.call('<', 3, 2)).toBe(false);
  });

  it('should compare >= operator', () => {
    expect(ExpressionRegistry.call('>=', 2, 2)).toBe(true);
    expect(ExpressionRegistry.call('>=', 1, 2)).toBe(false);
  });

  it('should compare <= operator', () => {
    expect(ExpressionRegistry.call('<=', 2, 2)).toBe(true);
    expect(ExpressionRegistry.call('<=', 3, 2)).toBe(false);
  });

  it('should compare === operator', () => {
    expect(ExpressionRegistry.call('===', 2, 2)).toBe(true);
    expect(ExpressionRegistry.call('===', 2, '2')).toBe(false);
  });

  it('should compare !== operator', () => {
    expect(ExpressionRegistry.call('!==', 2, '2')).toBe(true);
    expect(ExpressionRegistry.call('!==', 2, 2)).toBe(false);
  });

  it('should compare in operator with array', () => {
    expect(ExpressionRegistry.call('in', 'a', ['a', 'b'])).toBe(true);
    expect(ExpressionRegistry.call('in', 'c', ['a', 'b'])).toBe(false);
  });

  it('should compare in operator with string', () => {
    expect(ExpressionRegistry.call('in', 'a', 'a,b')).toBe(true);
    expect(ExpressionRegistry.call('in', 'c', 'a,b')).toBe(false);
  });

  it('should throw on unknown operator', () => {
    expect(() => {
      ExpressionRegistry.call('foobar', 1, 2);
    }).toThrow('Unknown operator "foobar"');
  });
});

describe('is helper', () => {
  let template, context, outTrue, outFalse;
  beforeEach(() => {
    outTrue = 'YES';
    outFalse = 'NO';
  });

  it('should support boolean context (args length 2)', () => {
    template = Handlebars.compile('{{#is foo}}YES{{else}}NO{{/is}}');
    context = { foo: true };
    expect(template(context)).toBe('YES');
    context = { foo: false };
    expect(template(context)).toBe('NO');
  });

  it('should support equality (args length 3)', () => {
    template = Handlebars.compile('{{#is foo bar}}YES{{else}}NO{{/is}}');
    context = { foo: 1, bar: 1 };
    expect(template(context)).toBe('YES');
    context = { foo: 1, bar: 2 };
    expect(template(context)).toBe('NO');
  });

  it('should support operator form (args length > 3)', () => {
    template = Handlebars.compile('{{#is foo ">" bar}}YES{{else}}NO{{/is}}');
    context = { foo: 2, bar: 1 };
    expect(template(context)).toBe('YES');
    context = { foo: 1, bar: 2 };
    expect(template(context)).toBe('NO');
  });

  it('should support "in" operator', () => {
    template = Handlebars.compile('{{#is foo "in" list}}YES{{else}}NO{{/is}}');
    context = { foo: 'a', list: ['a', 'b'] };
    expect(template(context)).toBe('YES');
    context = { foo: 'c', list: ['a', 'b'] };
    expect(template(context)).toBe('NO');
  });
});

describe('nl2br helper', () => {
  it('should convert newlines to <br>', () => {
    const template = Handlebars.compile('{{nl2br text}}');
    const result = template({ text: 'foo\nbar\r\nbaz' });
    expect(result).toMatch(/foo<br>(\n|\r\n)bar<br>(\n|\r\n)baz/);
  });

  it('should handle empty and falsy values', () => {
    const template = Handlebars.compile('{{nl2br text}}');
    expect(template({ text: '' })).toBe('');
    expect(template({ text: null })).toBe('null');
  });
});

describe('log helper', () => {
  it('calls console.log', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const template = Handlebars.compile('{{log 1 "two"}}');
    template({});
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
});

describe('debug helper', () => {
  it('calls console.log with context and values', () => {
    const spy = jest.spyOn(console, 'log').mockImplementation(() => {});
    const data = { foo: 'bar' };
    const template = Handlebars.compile('{{debug 1 "two"}}');
    template(data);
    expect(spy).toHaveBeenCalled();
    spy.mockRestore();
  });
});