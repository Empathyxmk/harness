// Public test for JSONCrush with different data

const {JSONCrush, JSONUncrush} = require('../JSONCrush.js');

describe('JSONCrush (public tests)', () => {
    it('should compress and decompress a deeply nested object with different values', () => {
        const testObj = {
            username: "Bob",
            score: 12345,
            achievements: ["gold", "silver", "bronze", "diamond"],
            settings: {darkMode: false, volume: 80, languages: ["fr", "es"], flags: null},
            meta: {verified: false, rank: 7}
        };
        const json = JSON.stringify(testObj);
        const crushed = JSONCrush(json);
        expect(typeof crushed).toBe('string');
        expect(crushed.length).toBeLessThan(json.length);
        const uncrushed = JSONUncrush(crushed);
        expect(uncrushed).toBe(json);
    });

    it('should not corrupt other simple numbers', () => {
        for (let n of [-1, 3.14, 1001, -273.15]) {
            const json = JSON.stringify(n);
            const crushed = JSONCrush(json);
            const uncrushed = JSONUncrush(crushed);
            expect(uncrushed).toBe(json);
        }
    });

    it('should work with different unicode and emoji', () => {
        const json = JSON.stringify("🐍🔥");
        const crushed = JSONCrush(json);
        const uncrushed = JSONUncrush(crushed);
        expect(uncrushed).toBe(json);
    });

    it('should handle edge case: null', () => {
        const json = JSON.stringify(null);
        expect(JSONUncrush(JSONCrush(json))).toBe(json);
    });

    it('should handle edge case: array with numbers', () => {
        const json = JSON.stringify([10, 20, 30, 40]);
        expect(JSONUncrush(JSONCrush(json))).toBe(json);
    });

    it('should handle edge case: object with no properties', () => {
        const json = JSON.stringify(Object.create(null)); // truly empty with no prototype
        expect(JSONUncrush(JSONCrush(json))).toBe(json);
    });
});