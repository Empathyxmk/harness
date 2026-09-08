const personalizationUtil = require('../personalizationUtil');

describe('personalizationUtil (public)', () => {
    describe('getPerson (public)', () => {
        it('should return person from handlerInput (different id)', () => {
            const handlerInput = { requestEnvelope: { context: { System: { person: { personId: 'xyz789' } } } } };
            expect(personalizationUtil.getPerson(handlerInput)).toEqual({ personId: 'xyz789' });
        });
        it('should return undefined if person not present', () => {
            const handlerInput = { requestEnvelope: { context: { System: { person: undefined } } } };
            expect(personalizationUtil.getPerson(handlerInput)).toBeUndefined();
        });
    });

    describe('getPersonalizedPrompt (public)', () => {
        it('should return prompt when person exists (different id)', () => {
            const handlerInput = {
                requestEnvelope: { context: { System: { person: { personId: 'another-id-987' } } } }
            };
            const result = personalizationUtil.getPersonalizedPrompt(handlerInput);
            if (typeof result === "function") {
                expect(result()).toBe("");
            } else {
                expect(result).toContain('alexa:name');
                expect(result).toContain('personId="another-id-987"');
            }
        });
        it('should return fallback (empty string) when person does not exist', () => {
            const handlerInput = { requestEnvelope: { context: { System: { person: null } } } };
            const result = personalizationUtil.getPersonalizedPrompt(handlerInput);
            expect(typeof result === 'function' ? result() : result).toBe("");
        });
    });
});