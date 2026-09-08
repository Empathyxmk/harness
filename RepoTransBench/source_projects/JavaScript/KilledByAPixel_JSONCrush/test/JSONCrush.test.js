// Existing test for JSONCrush

const {JSONCrush, JSONUncrush} = require('../JSONCrush.js');

describe('JSONCrush', () => {
    it('should compress and decompress a moderately sized object', () => {
        const testObj = {
            name: "Alice",
            age: 30,
            skills: ["js", "node", "python"],
            profile: {active: true, rating: 4.97},
        };
        const json = JSON.stringify(testObj);
        const crushed = JSONCrush(json);
        expect(typeof crushed).toBe('string');
        expect(crushed.length).toBeLessThan(json.length);
        const uncrushed = JSONUncrush(crushed);
        expect(uncrushed).toBe(json);
    });

    it('should not corrupt simple numbers', () => {
        for (let n of [0, 1, 12, 123.456]) {
            const json = JSON.stringify(n);
            const crushed = JSONCrush(json);
            const uncrushed = JSONUncrush(crushed);
            expect(uncrushed).toBe(json);
        }
    });

    it('should work with unique unicode and emoji', () => {
        const json = JSON.stringify("🦄𠜎");
        const crushed = JSONCrush(json);
        const uncrushed = JSONUncrush(crushed);
        expect(uncrushed).toBe(json);
    });

    it('should handle edge case: empty string', () => {
        const json = JSON.stringify("");
        expect(JSONUncrush(JSONCrush(json))).toBe(json);
    });

    it('should handle edge case: empty array', () => {
        const json = JSON.stringify([]);
        expect(JSONUncrush(JSONCrush(json))).toBe(json);
    });

    it('should handle edge case: empty object', () => {
        const json = JSON.stringify({});
        expect(JSONUncrush(JSONCrush(json))).toBe(json);
    });
});