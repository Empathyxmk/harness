const assert = (condition, message) => {
  if (!condition) {
    throw new Error(message);
  }
};

const asType = (type, opts = {}) => value => ({ type, value, ...opts });
const deferredType = (type, opts = {}) => {
  const typeFn = asType (type, opts);
  return typeFn (typeFn);
};

const deepCopy = o => {
  if (Array.isArray(o)) {
    return o.map(deepCopy);
  }
  if (Object.prototype.toString.call(o) === '[object Object]') {
    return Object.entries(o).reduce((acc, [k, v]) => {
      acc[k] = deepCopy(v);
      return acc;
    }, {});
  }
  return o;
}

const partition = (pred, a) => a.reduce((acc, cur) => {
  if (pred(cur)) {
    acc[0].push(cur);
  } else {
    acc[1].push(cur);
  }
  return acc;
}, [[], []]);

const specialChars = '\\.^$|?*+()[]{}-'.split('');
const replaceAll = (s, find, replace) => s.replace(new RegExp(`\\${find}`, 'g'), replace);
const escapeSpecial = s => specialChars.reduce((acc, char) => replaceAll(acc, char, `\\${char}`), s);

const namedGroupRegex = /^[a-z]+\w*$/i;
const singleUnicodeCharRegex = /^[^]$/u;
const controlCharRegex = /^[a-z]$/i;
const hexadecimalStringRegex = /^[0-9a-f]+$/i;

const quantifierTable = {
  oneOrMore: '+',
  oneOrMoreLazy: '+?',
  zeroOrMore: '*',
  zeroOrMoreLazy: '*?',
  optional: '?',
  exactly: times => `{${times}}`,
  atLeast: times => `{${times},}`,
  atLeastLazy: times => `{${times},}?`,
  between: times => `{${times[0]},${times[1]}}`,
  betweenLazy: times => `{${times[0]},${times[1]}}?`,
}

const applySubexpressionDefaults = expr => {
  const out = { ...expr };
  out.namespace = ('namespace' in out) ? out.namespace : '';
  out.ignoreFlags = ('ignoreFlags' in out) ? out.ignoreFlags : true;
  out.ignoreStartAndEnd = ('ignoreStartAndEnd' in out) ? out.ignoreStartAndEnd : true;

  assert(typeof out.namespace === 'string', 'namespace must be a string');
  assert(typeof out.ignoreFlags === 'boolean', 'ignoreFlags must be a boolean');
  assert(typeof out.ignoreStartAndEnd === 'boolean', 'ignoreStartAndEnd must be a boolean');

  return out;
}

// Expose for tests
module.exports = {
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
  hexadecimalStringRegex
};