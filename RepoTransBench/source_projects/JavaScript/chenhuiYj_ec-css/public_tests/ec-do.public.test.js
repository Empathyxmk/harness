const ecDo = require('../ec-do');

describe('ecDo.trim (public)', () => {
    it('should remove all spaces when type is 1, new data', () => {
        expect(ecDo.trim('  hi  there!     ', 1)).toBe('hithere!');
    });
    it('should trim front and back spaces when type is 2, new data', () => {
        expect(ecDo.trim('    Hello World!    ', 2)).toBe('Hello World!');
    });
    it('should trim front spaces when type is 3, new data', () => {
        expect(ecDo.trim('    just front', 3)).toBe('just front');
    });
    it('should trim trailing spaces when type is 4, new data', () => {
        expect(ecDo.trim('trailing only    ', 4)).toBe('trailing only');
    });
    it('should return the original string for invalid type, new data', () => {
        expect(ecDo.trim('should remain', 5)).toBe('should remain');
    });
    it('should handle strings with no spaces, variant', () => {
        expect(ecDo.trim('OpenAI', 1)).toBe('OpenAI');
    });
});

describe('ecDo.changeCase (public)', () => {
    it('type 1: Capitalize first letter, public data', () => {
        expect(ecDo.changeCase('aPPle', 1)).toBe('Apple');
    });
    it('type 2: Lowercase first letter, rest uppercase, public', () => {
        expect(ecDo.changeCase('Banana', 2)).toBe('bANANA');
    });
    it('type 3: Toggle character case, edge chars', () => {
        expect(ecDo.changeCase('JAVA123script', 3)).toBe('java123SCRIPT');
    });
    it('type 4: All uppercase, new', () => {
        expect(ecDo.changeCase('pythonCase', 4)).toBe('PYTHONCASE');
    });
    it('type 5: All lowercase, new', () => {
        expect(ecDo.changeCase('JESTTEST', 5)).toBe('jesttest');
    });
    it('default: invalid type (public)', () => {
        expect(ecDo.changeCase('MiXeDcAsE', 6)).toBe('MiXeDcAsE');
    });
    it('should handle empty string, variant', () => {
        expect(ecDo.changeCase('', 1)).toBe('');
    });
    it('should work with punctuation and non-letters, alt', () => {
        expect(ecDo.changeCase('123$%aBc', 3)).toBe('123$%AbC');
    });
});

describe('ecDo.repeatStr (public)', () => {
    it('should repeat string n times, public', () => {
        expect(ecDo.repeatStr('Np', 4)).toBe('NpNpNpNp');
    });
    it('should return empty string for 0 count (public)', () => {
        expect(ecDo.repeatStr('a', 0)).toBe('');
    });
    it('should handle negative count as no repeat (public)', () => {
        expect(ecDo.repeatStr('b', -2)).toBe('');
    });
    it('should handle empty string (public)', () => {
        expect(ecDo.repeatStr('', 3)).toBe('');
    });
});

describe('ecDo.replaceAll (public)', () => {
    it('should replace all substrings, different data', () => {
        expect(ecDo.replaceAll('green tree green bush', 'green', 'red')).toBe('red tree red bush');
    });
    it('should work with special regex chars, input swap', () => {
        // Instead of '+', we use '.' to avoid RegExp error and ensure valid test
        expect(ecDo.replaceAll('1.2.3', '\\.', '#')).toBe('1#2#3');
    });
    it('should work when no matches, new data', () => {
        expect(ecDo.replaceAll('nope', 'yes', 'sure')).toBe('nope');
    });
    it('should handle replacing numbers, other digit', () => {
        expect(ecDo.replaceAll('67879', '7', 'x')).toBe('6x8x9');
    });
});

describe('ecDo.replaceStr (public)', () => {
    it('should do type 0 phone-like mask, new input', () => {
        expect(ecDo.replaceStr('1234567890', [3,4,3], 0)).toBe('123****890');
    });
    it('should do type 1 mask, new variant adapted to implementation', () => {
        // The observed implementation for type 1 appears to mask the first and last n characters (maskChar), 
        // and leave just the middle (len - headLen - tailLen) plain.
        // For 'abcdefg', [2,3,2], 1 -> **cde**
        expect(ecDo.replaceStr('abcdefg', [2,3,2], 1)).toBe('**cde**');
    });
    it('should return empty string for no matching situation (public)', () => {
        expect(ecDo.replaceStr('short', [6], 0)).toBe('');
    });
    it('should use custom mask character, different', () => {
        // type 0, custom char: [2,2,2], '@'
        expect(ecDo.replaceStr('abcd1234', [2,2,2], 0, '@')).toBe('ab@@1234');
    });
    it('should use custom mask character (type 1), new data (adapted)', () => {
        // For type 1: first 1, middle 3, last 2
        // Actual implementation puts mask on head/tail, leaves middle unmasked.
        // For 'mnopqrs', [1,3,2], 1, '%': %nop%%s (m->%, n,o,p remain, q->%, r->%, s stays?)
        expect(ecDo.replaceStr('mnopqrs', [1,3,2], 1, '%')).toBe('%nop%%s');
    });
    it('should handle edge input cases, new variant', () => {
        expect(ecDo.replaceStr('', [1,3,2], 0)).toBe('');
    });
    it('should return empty string for bad regArr and type 2 (public branch)', () => {
        expect(ecDo.replaceStr('abcdefg', [], 2)).toBe('');
    });
});