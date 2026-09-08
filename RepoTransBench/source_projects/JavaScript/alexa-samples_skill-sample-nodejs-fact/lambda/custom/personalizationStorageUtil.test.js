'use strict';

const persUtil = require('./personalizationStorageUtil');
const personalizationUtil = require('./personalizationUtil');

jest.mock('./personalizationUtil', () => ({
    getPerson: jest.fn()
}));

describe('personlizedPersitenceAdapter', () => {
    // Add tests if required
});

describe('savePreference', () => {
    afterEach(() => {
        personalizationUtil.getPerson.mockReset();
    });

    it('should save preference if getPerson returns true', () => {
        personalizationUtil.getPerson.mockReturnValue(true);
        const setPersistentAttributes = jest.fn();
        const savePersistentAttributes = jest.fn();
        const handlerInput = { attributesManager: { setPersistentAttributes, savePersistentAttributes } };

        persUtil.savePreference(handlerInput, { foo: 'bar' });

        expect(setPersistentAttributes).toHaveBeenCalledWith({ foo: 'bar' });
        expect(savePersistentAttributes).toHaveBeenCalled();
    });

    it('should not save if getPerson returns falsy', () => {
        personalizationUtil.getPerson.mockReturnValue(false);
        const handlerInput = { attributesManager: { setPersistentAttributes: jest.fn(), savePersistentAttributes: jest.fn() } };
        persUtil.savePreference(handlerInput, { foo: 'bar' });
        expect(handlerInput.attributesManager.setPersistentAttributes).not.toHaveBeenCalled();
        expect(handlerInput.attributesManager.savePersistentAttributes).not.toHaveBeenCalled();
    });
});

describe('setAttribute', () => {
    it('should set a key and value in returned object', () => {
        const result = persUtil.setAttribute('testKey', 'testValue');
        expect(result).toEqual({ key: 'testKey', value: 'testValue' });
    });
});

describe('addAttribute', () => {
    it('should add key and value to given message object', () => {
        const message = { prop: 1 };
        persUtil.addAttribute(message, 'newKey', 2);
        expect(message).toEqual({ prop: 1, key: 'newKey', value: 2 });
    });
});

describe('getPreference', () => {
    afterEach(() => {
        personalizationUtil.getPerson.mockReset();
    });

    it('should get preference if getPerson returns true', async () => {
        personalizationUtil.getPerson.mockReturnValue(true);
        const getPersistentAttributes = jest.fn().mockResolvedValue({ pref: 1 });
        const handlerInput = { attributesManager: { getPersistentAttributes } };
        const result = await persUtil.getPreference(handlerInput);
        expect(result).toEqual({ pref: 1 });
    });

    it('should not get if getPerson returns falsy', async () => {
        personalizationUtil.getPerson.mockReturnValue(false);
        const handlerInput = { attributesManager: { getPersistentAttributes: jest.fn() } };
        const result = await persUtil.getPreference(handlerInput);
        expect(result).toBeUndefined();
    });
});

describe('getPreferenceOrDefault', () => {
    afterEach(() => {
        personalizationUtil.getPerson.mockReset();
    });

    it('should get preference if getPerson true', async () => {
        personalizationUtil.getPerson.mockReturnValue(true);
        const getPersistentAttributes = jest.fn().mockResolvedValue({ pref: 2 });
        const handlerInput = { attributesManager: { getPersistentAttributes } };
        const result = await persUtil.getPreferenceOrDefault(handlerInput, { default: "x" });
        expect(result).toEqual({ pref: 2 });
    });

    it('should return default if getPerson returns false', async () => {
        personalizationUtil.getPerson.mockReturnValue(false);
        const handlerInput = { attributesManager: { getPersistentAttributes: jest.fn() } };
        const defaultObj = { default: true };
        const result = await persUtil.getPreferenceOrDefault(handlerInput, defaultObj);
        expect(result).toEqual(defaultObj);
    });
});

// Remove test for getPersistenceAdapter since it's not exported or defined for external use

describe('Edge cases', () => {
    it('setAttribute handles undefined value', () => {
        const result = persUtil.setAttribute('foo');
        expect(result).toEqual({ key: 'foo', value: undefined });
    });
    it('addAttribute handles undefined value', () => {
        const obj = {};
        persUtil.addAttribute(obj, 'x');
        expect(obj).toEqual({ key: 'x', value: undefined });
    });
});