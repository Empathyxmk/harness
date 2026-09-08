const { ok, deepEqual }  = require('assert')
const {usecase, step, Ok, Err, request, entity, field, id} = require('../src/commonjs/herbs.cjs')

describe('A public use case', () => {

  describe('an alternative simple use case', () => {

    const anotherEntity = entity('anotherEntity', {
      value: id(Number),
      title: field(String)    
    })

    const givenAnotherUseCase = () => {
      const uc = usecase('Another use case', {
        'Init step': step(() => { return Ok() }),
        'Compound step': step({
          'part 1': step(() => { return Ok() }),
          'part 2': step(() => { return Ok() }),
        })
      })
      return uc
    }

    it('should return Ok for each step', async () => {
      // given
      const uc = givenAnotherUseCase()
      // when
      const response = await uc.run()
      // then
      ok(response.isOk)
    })
  })
})