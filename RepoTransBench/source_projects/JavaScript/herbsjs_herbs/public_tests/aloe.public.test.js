const {spec, scenario, given, when, check, state} = require('../src/commonjs/herbs.cjs').specs
const assert = require('assert')

describe('A public spec', () => {
  context('generic', () => {
    context('before run', () => {
      const givenTheSimplestGenericSpecPublic = () => {
        const ASpec = spec({
          'Another scenario': scenario({
            info: 'Another scenario',
            'Given other input': given(() => ({
              num: 42,
            })),
            'When running alternative': when((ctx) => {
              ctx.num = 100
            }),
            'Check another output public': check((ctx) => {
              assert.ok(ctx.num === 100)
            }),
          }),
        })
        return ASpec
      }

      it('should run and validate for public data', async () => {
        // given
        const ASpec = givenTheSimplestGenericSpecPublic()
        // when
        await ASpec()
        // then (assertion in check step)
      })
    })
  })
})