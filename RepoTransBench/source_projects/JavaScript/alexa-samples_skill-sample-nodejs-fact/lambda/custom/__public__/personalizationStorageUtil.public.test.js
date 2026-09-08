'use strict';

const persUtil = require('../personalizationStorageUtil');
const personalizationUtil = require('../personalizationUtil');

jest.mock('../personalizationUtil', () => ({
    getPerson: jest.fn()
}));

describe('personlizedPersitenceAdapter (public)', () => {
    // No public tests as in the original.
});

describe('savePreference (public)', () => {
    afterEach(() => {
        personalizationUtil.getPerson.mockReset();
    });

    it('should save preference if getPerson returns true (different key/val)', () => {
        personalizationUtil.getPerson.mockReturnValue(true);
        const setPersistentAttributes = jest.fn();
        const savePersistentAttributes = jest.fn();
        const handlerInput = { attributesManager: { setPersistentAttributes, savePersistentAttributes } };

        persUtil.savePreference(handlerInput, { baz: 'qux' });

        expect(setPersistentAttributes).toHaveBeenCalledWith({ baz: 'qux' });
        expect(savePersistentAttributes).toHaveBeenCalled();
    });

    it('should not save if getPerson returns falsy', () => {
        personalizationUtil.getPerson.mockReturnValue(undefined);
        const handlerInput = { attributesManager: { setPersistentAttributes: jest.fn(), savePersistentAttributes: jest.fn() } };
        persUtil.savePreference(handlerInput, { baz: 'qux' });
        expect(handlerInput.attributesManager.setPersistentAttributes).not.toHaveBeenCalled();
        expect(handlerInput.attributesManager.savePersistentAttributes).not.toHaveBeenCalled();
    });
});

describe('setAttribute (public)', () => {
    it('should set a key and value in returned object (different key/val)', () => {
        const result = persUtil.setAttribute('alpha', 'beta');
        expect(result).toEqual({ key: 'alpha', value: 'beta' });
    });
});

describe('addAttribute (public)', () => {
    it('should add key and value to given message object (changed values)', () => {
        const message = { another: 10 };
        persUtil.addAttribute(message, 'plusKey', 20);
        expect(message).toEqual({ another: 10, key: 'plusKey', value: 20 });
    });
});

describe('getPreference (public)', () => {
    afterEach(() => {
        personalizationUtil.getPerson.mockReset();
    });

    it('should get preference if getPerson returns true (different data)', async () => {
        personalizationUtil.getPerson.mockReturnValue(true);
        const getPersistentAttributes = jest.fn().mockResolvedValue({ custom: 42 });
        const handlerInput = { attributesManager: { getPersistentAttributes } };
        const result = await persUtil.getPreference(handlerInput);
        expect(result).toEqual({ custom: 42 });
    });

    it('should not get if getPerson returns falsy', async () => {
        personalizationUtil.getPerson.mockReturnValue(null);
        const handlerInput = { attributesManager: { getPersistentAttributes: jest.fn() } };
        const result = await persUtil.getPreference(handlerInput);
        expect(result).toBeUndefined();
    });
});

describe('getPreferenceOrDefault (public)', () => {
    afterEach(() => {
        personalizationUtil.getPerson.mockReset();
    });

    it('should get preference if getPerson true (other value)', async () => {
        personalizationUtil.getPerson.mockReturnValue(true);
        const getPersistentAttributes = jest.fn().mockResolvedValue({ pref: 99 });
        const handlerInput = { attributesManager: { getPersistentAttributes } };
        const result = await persUtil.getPreferenceOrDefault(handlerInput, { default: "y" });
        expect(result).toEqual({ pref: 99 });
    });

    it('should return default if getPerson returns false', async () => {
        personalizationUtil.getPerson.mockReturnValue(false);
        const handlerInput = { attributesManager: { getPersistentAttributes: jest.fn() } };
        const defaultObj = { foo: 'bar' };
        const result = await persUtil.getPreferenceOrDefault(handlerInput, defaultObj);
        expect(result).toEqual(defaultObj);
    });
});

describe('Edge cases (public)', () => {
    it('setAttribute handles undefined value (diff key)', () => {
        const result = persUtil.setAttribute('foozle');
        expect(result).toEqual({ key: 'foozle', value: undefined });
    });
    it('addAttribute handles undefined value (diff key)', () => {
        const obj = {};
        persUtil.addAttribute(obj, 'yolo');
        expect(obj).toEqual({ key: 'yolo', value: undefined });
    });
});