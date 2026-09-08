const ecDo = require('./ec-do.js');

describe('ecDo.trim', () => {
    it('should remove all spaces when type is 1', () => {
        expect(ecDo.trim('  ab c  ', 1)).toBe('abc');
    });
    it('should trim front and back spaces when type is 2', () => {
        expect(ecDo.trim('  ab c  ', 2)).toBe('ab c');
    });
    it('should trim front spaces when type is 3', () => {
        expect(ecDo.trim('  ab c  ', 3)).toBe('ab c  ');
    });
    it('should trim trailing spaces when type is 4', () => {
        expect(ecDo.trim('  ab c  ', 4)).toBe('  ab c');
    });
    it('should return the original string for invalid type', () => {
        expect(ecDo.trim('  ab c  ', 99)).toBe('  ab c  ');
    });
    it('should handle strings with no spaces', () => {
        expect(ecDo.trim('abc', 1)).toBe('abc');
        expect(ecDo.trim('abc', 2)).toBe('abc');
        expect(ecDo.trim('', 2)).toBe('');
    });
});

describe('ecDo.changeCase', () => {
    it('type 1: Capitalize first letter', () => {
        expect(ecDo.changeCase('hello world', 1)).toBe('Hello World');
    });
    it('type 2: Lowercase first letter, rest uppercase', () => {
        expect(ecDo.changeCase('Hello World', 2)).toBe('hELLO wORLD');
    });
    it('type 3: Toggle character case', () => {
        expect(ecDo.changeCase('AbC1x#', 3)).toBe('aBc1X#');
    });
    it('type 4: All uppercase', () => {
        expect(ecDo.changeCase('aBc', 4)).toBe('ABC');
    });
    it('type 5: All lowercase', () => {
        expect(ecDo.changeCase('aBC', 5)).toBe('abc');
    });
    it('default: invalid type', () => {
        expect(ecDo.changeCase('Hello', 999)).toBe('Hello');
    });
    it('should handle empty string', () => {
        expect(ecDo.changeCase('', 1)).toBe('');
    });
    it('should work with punctuation and non-letters', () => {
        expect(ecDo.changeCase('hi! BYE', 3)).toBe('HI! bye');
    });
});

describe('ecDo.repeatStr', () => {
    it('should repeat string n times', () => {
        expect(ecDo.repeatStr('ab', 3)).toBe('ababab');
    });
    it('should return empty string for 0 count', () => {
        expect(ecDo.repeatStr('x', 0)).toBe('');
    });
    it('should handle negative count as no repeat', () => {
        expect(ecDo.repeatStr('a', -1)).toBe('');
    });
    it('should handle empty string', () => {
        expect(ecDo.repeatStr('', 5)).toBe('');
    });
});

describe('ecDo.replaceAll', () => {
    it('should replace all substrings', () => {
        expect(ecDo.replaceAll('aa-bb-aa', 'aa', 'xx')).toBe('xx-bb-xx');
    });
    it('should work with special regex chars', () => {
        expect(ecDo.replaceAll('a.b.c', '\\.', '-')).toBe('a-b-c');
    });
    it('should work when no matches', () => {
        expect(ecDo.replaceAll('abc', 'x', 'z')).toBe('abc');
    });
    it('should handle replacing numbers', () => {
        expect(ecDo.replaceAll('123123', '1', 'x')).toBe('x23x23');
    });
});

describe('ecDo.replaceStr', () => {
    it('should do type 0 phone-like mask', () => {
        expect(ecDo.replaceStr('18819322663', [3,5,3], 0)).toBe('188*****663');
    });
    it('should do type 1 email-like mask (matches likely implementation)', () => {
        expect(ecDo.replaceStr('abcdefghijz', [3,5,3], 1)).toBe('***defgh***');
    });
    it('should return empty string for no matching situation', () => {
        expect(ecDo.replaceStr('abc', [1], 0)).toBe('');
    });
    it('should use custom mask character', () => {
        expect(ecDo.replaceStr('123456789', [2,3,2], 0, '#')).toBe('12###6789');
    });
    it('should use custom mask character (type 1)', () => {
        expect(ecDo.replaceStr('abcdefgh', [2,3,2], 1, '#')).toBe('##cde##h');
    });
    it('should handle edge input cases', () => {
        expect(ecDo.replaceStr('', [2,3,2], 0)).toBe('');
        expect(ecDo.replaceStr('', [2,3,2], 1)).toBe('');
    });
    it('should return empty string for bad regArr and type 2 (untested branch)', () => {
        expect(ecDo.replaceStr('abc', [1,2], 2)).toBe('');
    });
});