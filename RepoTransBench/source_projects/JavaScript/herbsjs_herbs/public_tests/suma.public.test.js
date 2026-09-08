const assert = require('assert')
const {validate} = require('../src/commonjs/herbs.cjs')


describe('public suma', () => {

    describe('valid validators with different values', () => {

        it('multiple validators with another valid value', () => {
            const value = 'demo'
            const validations = {
                presence: true,
                allowNull: false,
                type: String,
                length: {
                    minimum: 3,
                    maximum: 5,
                    is: 4
                }
            }

            const result = validate(value, validations)
            assert.strictEqual(result, undefined)
        })

    })
})