const { supportsInterface, supportsAPL } = require('./index');

describe('supportsInterface', () => {
    it('returns true when interface is explicitly present and not null/undefined', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: { "Alexa.Presentation.APL": {} }
                        }
                    }
                }
            }
        };
        expect(supportsInterface(handlerInput, 'Alexa.Presentation.APL')).toBe(true);
    });

    it('returns false when interface is undefined', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: {}
                        }
                    }
                }
            }
        };
        expect(supportsInterface(handlerInput, 'Alexa.Presentation.APL')).toBe(false);
    });

    it('handles missing properties safely (null nested)', () => {
        [
            {},
            { requestEnvelope: {} },
            { requestEnvelope: { context: {} } },
            { requestEnvelope: { context: { System: {} } } },
            { requestEnvelope: { context: { System: { device: {} } } } }
        ].forEach(obj => {
            expect(supportsInterface(obj, 'Alexa.Presentation.APL')).toBe(false);
        });
    });

    it('returns false if the interface entry is null', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: { "Alexa.Presentation.APL": null }
                        }
                    }
                }
            }
        };
        expect(supportsInterface(handlerInput, 'Alexa.Presentation.APL')).toBe(false);
    });
});

describe('supportsAPL', () => {
    it('returns true when supported', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: { "Alexa.Presentation.APL": { something: true } }
                        }
                    }
                }
            }
        };
        expect(supportsAPL(handlerInput)).toBe(true);
    });
    it('returns false when not supported', () => {
        const handlerInput = {
            requestEnvelope: {
                context: {
                    System: {
                        device: {
                            supportedInterfaces: {}
                        }
                    }
                }
            }
        };
        expect(supportsAPL(handlerInput)).toBe(false);
    });
});