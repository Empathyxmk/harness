/**
 * zz_spellfucker - Igor Pavlov
 * The MIT License (MIT)
 *
 * This is a fun, "obfuscate-like" implementation.
 */
(function (root, factory) {
  if (typeof exports === "object") {
    module.exports = factory();
  } else if (typeof define === "function" && define.amd) {
    define(factory);
  } else {
    root.spellfucker = factory();
  }
}(typeof self !== 'undefined' ? self : this, function () {
  // Patch: Accept only string-like, return '' for null/undefined/non-string
  function coerceStr(str) {
    if (typeof str === 'string') return str;
    if (str === null || str === undefined) return '';
    // Accept numbers, booleans, but not objects/arrays/functions
    if (typeof str === 'number' || typeof str === 'boolean') return String(str);
    // Otherwise, skip
    return '';
  }

  // Main spellfucker core (original)
  const replacements = [
    // Sibilant consonants
    [/(ss+)/g, 's'], // ss → s
    [/(zz+)/g, 'z'], // zz → z
    [/(ch)+/g, 'ć'],
    // Some more fun replacements
    [/ph/g, 'f'],
    [/ough/g, 'uf'],
    [/ght/g, 't'],
    [/wr/g, 'r'],
    [/kn/g, 'n'],
    [/qu/g, 'kw'],
    [/(tio)n/g, 'shun'],
    [/ea/g, 'i'],
    [/th/g, 'z'],
    //... can be expanded
  ];

  // A more complex fun matrix, for test coverage
  const regexpMatrix = [
    [/(bb)/g, 'b'], [/(cc)/g, 'c'], [/(ff)/g, 'f'], [/(ll)/g, 'l'],
    [/(mm)/g, 'm'], [/(nn)/g, 'n'], [/(pp)/g, 'p'], [/(rr)/g, 'r'],
    [/gue/g, 'g'], [/gn/g, 'n'], [/wh/g, 'w'], [/^h(?!o)/g, ''], [/ho/g, 'o'],
    [/dge/g, 'j'], [/j/g, 'dzh'], [/k/g, 'c'], [/c/g, 'k'],
    [/sc/g, 'sk'], [/ss/g, 's'],
    [/m$/g, ''], [/n$/g, ''], [/g$/g, ''], [/ng$/g, 'n'],
    [/v$/g, 'f'],
    [/ce$/g, 's'], [/t$/g, 'd'],
    [/^n/g, ''],
    [/^w([^h])/g, '$1'],
    // ... more chars
    [/y/g, 'i']
  ];

  function mutate(word) {
    let w = word;
    for (let i = 0; i < replacements.length; ++i) {
      w = w.replace(replacements[i][0], replacements[i][1]);
    }
    for (let i = 0; i < regexpMatrix.length; ++i) {
      w = w.replace(regexpMatrix[i][0], regexpMatrix[i][1]);
    }
    return w;
  }

  const obfuscate = function (string, options) {
    string = coerceStr(string);

    options = options || {};
    const lines = string.split(/\n/); // Defensive: string is always string

    const obfuscatedLines = [];
    for (var l = 0; l < lines.length; l++) {
      const line = lines[l];
      const words = line.split(/\b/);
      const obsWords = [];
      for (var w = 0; w < words.length; w++) {
        let word = words[w];
        // anti-dumb: only mutate words longer than 1 char, and mostly alphabet
        if (/^[A-Za-z]{2,}$/.test(word)) {
          word = mutate(word);
        }
        obsWords.push(word);
      }
      obfuscatedLines.push(obsWords.join(''));
    }

    return obfuscatedLines.join('\n');
  };

  return obfuscate;
}));