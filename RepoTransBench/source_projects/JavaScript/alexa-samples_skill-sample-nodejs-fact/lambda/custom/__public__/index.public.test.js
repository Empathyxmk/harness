const { supportsInterface } = require('../index');

describe('supportsInterface (public)', () => {
    it('should return true if interface is supported (with different interface)', () => {
        // Use different interface name and envelope variants
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: {
                                'AudioPlayer': {}
                            }
                        }
                    }
                }
            }
        };
        expect(supportsInterface(handlerInput, 'AudioPlayer')).toEqual(true);
        expect(supportsInterface(handlerInput, 'Display')).toEqual(false);
    });

    it('should return false if handlerInput is falsy or not an object', () => {
        // skip null/undefined: test only {} and primitive types
        expect(supportsInterface({}, 'AudioPlayer')).toEqual(false);
        expect(supportsInterface('', 'Display')).toEqual(false);
        expect(supportsInterface(0, 'VideoApp')).toEqual(false);
        expect(supportsInterface(false, 'VideoApp')).toEqual(false);
    });

    it('should handle missing properties safely, deeper variations', () => {
        // Provide handlerInput with empty requestEnvelope
        expect(supportsInterface({ requestEnvelope: {} }, 'AudioPlayer')).toEqual(false);

        // Provide handlerInput with requestEnvelope.context missing
        expect(supportsInterface({ requestEnvelope: { context: null } }, 'AudioPlayer')).toEqual(false);

        // Provide handlerInput with device missing
        expect(supportsInterface({ requestEnvelope: { context: { System: {} } } }, 'AudioPlayer')).toEqual(false);

        // Provide handlerInput with supportedInterfaces missing
        expect(supportsInterface({ requestEnvelope: { context: { System: { device: {} } } } }, 'AudioPlayer')).toEqual(false);
    });

    it('should check a custom user interface (changed test)', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: {
                                'CustomInterface': {},
                                'VideoApp': {}
                            }
                        }
                    }
                }
            }
        };
        expect(supportsInterface(handlerInput, 'CustomInterface')).toEqual(true);
        expect(supportsInterface(handlerInput, 'VideoApp')).toEqual(true);
        expect(supportsInterface(handlerInput, 'GameEngine')).toEqual(false);
    });

    it('should work for interfaces with odd property names', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: {
                                'myWeird-Interface_B56': {}
                            }
                        }
                    }
                }
            }
        };
        expect(supportsInterface(handlerInput, 'myWeird-Interface_B56')).toEqual(true);
        expect(supportsInterface(handlerInput, 'AnotherOne')).toEqual(false);
    });
});