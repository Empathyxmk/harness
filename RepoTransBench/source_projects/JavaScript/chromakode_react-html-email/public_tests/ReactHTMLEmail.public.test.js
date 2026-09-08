describe('ReactHTMLEmail (public)', () => {
  let module
  let checkPropTypes

  beforeEach(() => {
    jest.restoreAllMocks()
    jest.resetModules()
    module = require('../src/index')
    checkPropTypes = require('prop-types').checkPropTypes
  })

  describe('PropTypes.style (public)', () => {
    it('returns an error for non-objects (different input data)', () => {
      const spy = jest.spyOn(console, 'error').mockImplementation()
      const style = 'not-an-object'
      checkPropTypes(module.PropTypes, { style }, 'style', 'TestPublic')
      expect(spy).toHaveBeenCalled()
      expect(spy).toHaveBeenCalledWith('Warning: Failed style type: Invalid style `style` of type `string` supplied to `TestPublic`, expected `object`.')
    })

    it('validates different style objects', () => {
      const spy = jest.spyOn(module.default.styleValidator, 'validate').mockImplementation()
      const style = { padding: '5px' }
      checkPropTypes(module.PropTypes, { style }, 'style', 'TestPublic')
      expect(spy).toHaveBeenCalledWith(style, 'TestPublic')
    })
  })

  describe('configStyleValidator (public)', () => {
    it('updates StyleValidator config with different config', () => {
      const spy = jest.spyOn(module.default.styleValidator, 'setConfig').mockImplementation()
      const config = { strict: true }
      module.configStyleValidator(config)
      expect(spy).toHaveBeenCalledWith(config)
    })
  })

  describe('when NODE_ENV=production (public)', () => {
    let origENV

    beforeAll(() => {
      origENV = process.env.NODE_ENV
      process.env.NODE_ENV = 'production'
    })

    it('still disables warnings in production', () => {
      expect(module.default.styleValidator.config.warn).toEqual(false)
    })

    afterAll(() => {
      process.env.NODE_ENV = origENV
    })
  })
})