const assert  = require('assert')
const {entity, field, id} = require('../src/commonjs/herbs.cjs')

describe('A public entity', () => {

    describe('an alternative entity', () => {

        const givenAnotherEntity = () => {
            const AnotherEntity = entity('Another entity', {
                altField1: field(Number),
                altField2: id(Number)
            })
            return new AnotherEntity()
        }

        it('should initiate with public data', () => {
            //given
            const instance = givenAnotherEntity()
            //then
            assert.equal(instance.meta.name, 'Another entity')
        })
    })
})