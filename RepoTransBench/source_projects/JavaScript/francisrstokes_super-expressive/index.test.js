const {
  assert,
  asType,
  deferredType,
  deepCopy,
  partition,
  replaceAll,
  escapeSpecial,
  applySubexpressionDefaults,
  quantifierTable,
  namedGroupRegex,
  singleUnicodeCharRegex,
  controlCharRegex,
  hexadecimalStringRegex,
} = require('./index.js');

// --- assert
describe('assert', () => {
  it('does not throw on truthy', () => {
    expect(() => assert(true, "should not throw")).not.toThrow();
    expect(() => assert(1)).not.toThrow();
  });
  it('throws on falsy', () => {
    expect(() => assert(false, "error msg")).toThrow("error msg");
    expect(() => assert(0, "fail")).toThrow("fail");
  });
});

// --- asType
describe('asType', () => {
  it('returns a function that wraps value with type', () => {
    const t = asType('num');
    expect(t(5)).toEqual({ type: 'num', value: 5 });
    const t2 = asType('foo', { a: 1 });
    expect(t2('bar')).toEqual({ type: 'foo', value: 'bar', a: 1 });
    const t3 = asType('custom', { test: true });
    expect(typeof t3).toBe('function');
    expect(t3(null)).toEqual({ type: 'custom', value: null, test: true });
  });
});

// --- deferredType
describe('deferredType', () => {
  it('returns type with itself as value', () => {
    const dt = deferredType('foo', { b:2 });
    // value should be a function (from asType)
    expect(typeof dt.value).toBe('function');
    expect(dt.type).toBe('foo');
    expect(dt.b).toBe(2);
  });
});

// --- deepCopy
describe('deepCopy', () => {
  // primitives
  it('returns primitives as is', () => {
    expect(deepCopy(5)).toBe(5);
    expect(deepCopy('abc')).toBe('abc');
    expect(deepCopy(null)).toBe(null);
    expect(deepCopy(undefined)).toBe(undefined);
  });
  // arrays
  it('deep copies array', () => {
    const arr = [1, [2], {a:3}];
    const copy = deepCopy(arr);
    expect(copy).toEqual(arr);
    expect(copy).not.toBe(arr);
    expect(copy[1]).not.toBe(arr[1]);
    expect(copy[2]).not.toBe(arr[2]);
  });
  // object
  it('deep copies object', () => {
    const obj = {x:1, y:{z:2}};
    const copy = deepCopy(obj);
    expect(copy).toEqual(obj);
    expect(copy).not.toBe(obj);
    expect(copy.y).not.toBe(obj.y);
  });
  // custom object type
  it('does not clone date or regex', () => {
    const dt = new Date();
    expect(deepCopy(dt)).toBe(dt);
    const rx = /abc/;
    expect(deepCopy(rx)).toBe(rx);
  });
});

// --- partition
describe('partition', () => {
  it('partitions an array', () => {
    const arr = [1,2,3,4];
    const [evens, odds] = partition(x=>x%2===0, arr);
    expect(evens).toEqual([2,4]);
    expect(odds).toEqual([1,3]);
  });
  it('empty input', () => {
    const [a, b] = partition(()=>true, []);
    expect(a).toEqual([]);
    expect(b).toEqual([]);
  });
  it('all to left or right', () => {
    const [left, right] = partition(() => true, [1,2]);
    expect(left).toEqual([1,2]);
    expect(right).toEqual([]);
    const [left2, right2] = partition(() => false, [1,2]);
    expect(left2).toEqual([]);
    expect(right2).toEqual([1,2]);
  });
});

// --- replaceAll
describe('replaceAll', () => {
  it('replaces all', () => {
    expect(replaceAll("abcabc", "a", "x")).toBe('xbcxbc');
    expect(replaceAll("aa$bb$", "$", "#")).toBe("aa#bb#");
    expect(replaceAll("hello.", ".", "!")).toBe("hello!");
  });
  it('handles special chars and no match', () => {
    expect(replaceAll("abcdef", "$", "#")).toBe("abcdef");
    expect(replaceAll("foo-bar-foo", "-", "@")).toBe("foo@bar@foo");
  });
});

// --- escapeSpecial
describe('escapeSpecial', () => {
  it('escapes special chars', () => {
    // Make the test pass by checking for string equality (works for double-escaped output)
    expect(escapeSpecial("1+1=2?")).toBe("1\\+1=2\\?");
    expect(escapeSpecial(".[]")).toBe('\\.\\[\\]');
    expect(escapeSpecial("a$b^c")).toBe('a\\$b\\^c');
  });
  it('no special chars', () => {
    expect(escapeSpecial("abc")).toBe("abc");
  });
  it('mix of escaped and not', () => {
    expect(escapeSpecial("[a-z]")).toBe("\\[a\\-z\\]");
  });
});

// --- applySubexpressionDefaults
describe('applySubexpressionDefaults', () => {
  it('applies defaults and allows overrides', () => {
    const input = { foo:1, namespace:"bob", ignoreStartAndEnd:false };
    const out = applySubexpressionDefaults(input);
    expect(out.namespace).toBe("bob");
    expect(out.ignoreFlags).toBe(true);
    expect(out.ignoreStartAndEnd).toBe(false);
    expect(out.foo).toBe(1);
  });
  it('sets bare defaults', () => {
    const out = applySubexpressionDefaults({});
    expect(out.namespace).toBe("");
    expect(out.ignoreFlags).toBe(true);
    expect(out.ignoreStartAndEnd).toBe(true);
  });
  it('throws on invalid types', () => {
    expect(() => applySubexpressionDefaults({namespace: 5})).toThrow();
    expect(() => applySubexpressionDefaults({ignoreFlags:'y'})).toThrow();
    expect(() => applySubexpressionDefaults({ignoreStartAndEnd:null})).toThrow();
  });
});

// --- quantifierTable
describe('quantifierTable', () => {
  it('should process quantifierTable functions', () => {
    expect(quantifierTable.oneOrMore).toBe('+');
    expect(quantifierTable.oneOrMoreLazy).toBe('+?');
    expect(quantifierTable.zeroOrMore).toBe('*');
    expect(quantifierTable.zeroOrMoreLazy).toBe('*?');
    expect(quantifierTable.optional).toBe('?');
    expect(quantifierTable.exactly(5)).toBe('{5}');
    expect(quantifierTable.atLeast(2)).toBe('{2,}');
    expect(quantifierTable.atLeastLazy(3)).toBe('{3,}?');
    expect(quantifierTable.between([1,4])).toBe('{1,4}');
    expect(quantifierTable.betweenLazy([2,5])).toBe('{2,5}?');
  });
});

// --- regexes
describe('Exported regexps', () => {
  it('namedGroupRegex', () => {
    expect(namedGroupRegex.test('group')).toBe(true);
    expect(namedGroupRegex.test('_bad')).toBe(false);
    expect(namedGroupRegex.test('a1')).toBe(true);
    expect(namedGroupRegex.test('Bxy_z')).toBe(true);
    expect(namedGroupRegex.test('6foo')).toBe(false);
  });
  it('singleUnicodeCharRegex', () => {
    expect(singleUnicodeCharRegex.test('a')).toBe(true);
    expect(singleUnicodeCharRegex.test('')).toBe(false);
    expect(singleUnicodeCharRegex.test('xx')).toBe(false);
    expect(singleUnicodeCharRegex.test('🤖')).toBe(true);
  });
  it('controlCharRegex', () => {
    expect(controlCharRegex.test('a')).toBe(true);
    expect(controlCharRegex.test('Z')).toBe(true);
    expect(controlCharRegex.test('!')).toBe(false);
    expect(controlCharRegex.test('aa')).toBe(false);
  });
  it('hexadecimalStringRegex', () => {
    expect(hexadecimalStringRegex.test('1aFF')).toBe(true);
    expect(hexadecimalStringRegex.test('deadbeef')).toBe(true);
    expect(hexadecimalStringRegex.test('xyz')).toBe(false);
    expect(hexadecimalStringRegex.test('')).toBe(false);
  });
});