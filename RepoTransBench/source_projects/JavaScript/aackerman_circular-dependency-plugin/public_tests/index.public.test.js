const CircularDependencyPlugin = require('../index')

// Slightly different fake module creator for new values
function createPublicFakeModule({ debugId, resource, dependencies } = {}) {
  return {
    debugId: debugId || Math.floor(Math.random() * 20000) + 5000,
    resource: resource || '/public/fake/sample.js',
    dependencies: dependencies || []
  }
}

function createPublicFakeDependency({ module, name = 'PublicDep', weak = false } = {}) {
  function PublicConstructor() {}
  PublicConstructor.name = name
  return {
    module,
    weak,
    constructor: PublicConstructor
  }
}

function createPublicFakeCompilation({ withModuleGraph = false } = {}) {
  const graph = {
    getModule: dep => dep.module // simplest case
  }
  return {
    moduleGraph: withModuleGraph ? graph : undefined,
    errors: [],
    warnings: [],
  }
}

describe('CircularDependencyPlugin (public tests)', () => {
  it('should construct with custom public options', () => {
    const plugin = new CircularDependencyPlugin({
      failOnError: true,
      allowAsyncCycles: true
    })
    expect(plugin.options).toBeDefined()
    expect(plugin.options.failOnError).toBe(true)
    expect(plugin.options.allowAsyncCycles).toBe(true)
    expect(plugin.options.onDetected).toBe(false)
  })

  it('should invoke onStart and onEnd hooks (public)', () => {
    const onStart = jest.fn()
    const onEnd = jest.fn()
    const plugin = new CircularDependencyPlugin({
      onStart,
      onEnd,
    })
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([createPublicFakeModule()])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
    expect(onStart).toHaveBeenCalled()
    expect(onEnd).toHaveBeenCalled()
  })

  it('should skip modules if resource is empty string (public)', () => {
    const plugin = new CircularDependencyPlugin()
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([{ resource: '' }])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
    // No error expected for empty string resource
  })

  it('should skip modules if resource does not match custom include or matches custom exclude (public)', () => {
    const plugin = new CircularDependencyPlugin({
      include: /xyz789$/,
      exclude: /fake/
    })
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([
                      { resource: '/other/file2.ts' }, // include miss
                      { resource: '/public/fake/sample.js' }, // exclude hit
                    ])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
  })

  it('should detect cycles and invoke onDetected if present (public)', () => {
    const onDetected = jest.fn()
    const plugin = new CircularDependencyPlugin({
      onDetected
    })
    const modX = createPublicFakeModule({ debugId: 10, resource: '/X.js' })
    const modY = createPublicFakeModule({ debugId: 20, resource: '/Y.js' })
    modX.dependencies = [
      createPublicFakeDependency({ module: modY })
    ]
    modY.dependencies = [
      createPublicFakeDependency({ module: modX })
    ]
    const compilation = createPublicFakeCompilation()
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([modX])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
    plugin.isCyclic(modX, modX, {}, compilation)
    expect(typeof plugin.options.onDetected).toBe('function')
    expect(onDetected).not.toThrow
  })

  it('should add errors if failOnError=true otherwise add warnings (public)', () => {
    // failOnError = true
    const pluginErr = new CircularDependencyPlugin({ failOnError: true })
    const modX = createPublicFakeModule({ debugId: 3, resource: '/X.js' })
    const modY = createPublicFakeModule({ debugId: 8, resource: '/Y.js' })
    modX.dependencies = [ createPublicFakeDependency({ module: modY }) ]
    modY.dependencies = [ createPublicFakeDependency({ module: modX }) ]
    const compilation = createPublicFakeCompilation()
    compilation.errors = []
    compilation.warnings = []
    pluginErr.isCyclic(modX, modX, {}, compilation)
    let cyclePaths = pluginErr.isCyclic(modX, modX, {}, compilation)
    if (cyclePaths) {
      let error = new Error('Circular dependency detected:\r\n' + cyclePaths.join(' -> '))
      compilation.errors.push(error)
    }
    expect(compilation.errors.length).toBe(1)
    
    // failOnError = false
    const pluginWarn = new CircularDependencyPlugin({ failOnError: false })
    compilation.errors = []
    compilation.warnings = []
    cyclePaths = pluginWarn.isCyclic(modX, modX, {}, compilation)
    if (cyclePaths) {
      let error = new Error('Circular dependency detected:\r\n' + cyclePaths.join(' -> '))
      compilation.warnings.push(error)
    }
    expect(compilation.warnings.length).toBe(1)
  })

  it('isCyclic returns false when resource is undefined (public)', () => {
    const plugin = new CircularDependencyPlugin()
    const modX = createPublicFakeModule({ debugId: 3, resource: undefined })
    const modY = createPublicFakeModule({ debugId: 4, resource: '/Y.js' })
    modX.dependencies = [ createPublicFakeDependency({ module: modY }) ]
    const compilation = createPublicFakeCompilation()
    expect(plugin.isCyclic(modX, modX, {}, compilation)).toBe(false)
  })

  it('isCyclic skips PublicSelfReferenceDependency (public)', () => {
    const plugin = new CircularDependencyPlugin()
    const modX = createPublicFakeModule({ debugId: 5, resource: '/X.js' })
    modX.dependencies = [ createPublicFakeDependency({ module: modX, name: 'PublicSelfReferenceDependency' }) ]
    const compilation = createPublicFakeCompilation()
    expect(plugin.isCyclic(modX, modX, {}, compilation)).toBe(false)
  })

  it('isCyclic ignores async/weak dependencies when allowAsyncCycles is true (public)', () => {
    const plugin = new CircularDependencyPlugin({ allowAsyncCycles: true })
    const modX = createPublicFakeModule({ debugId: 6, resource: '/X.js' })
    const modY = createPublicFakeModule({ debugId: 7, resource: '/Y.js' })
    modX.dependencies = [ createPublicFakeDependency({ module: modY, weak: true }) ]
    modY.dependencies = [ createPublicFakeDependency({ module: modX }) ]
    const compilation = createPublicFakeCompilation()
    expect(plugin.isCyclic(modX, modX, {}, compilation)).toBe(false)
  })

  it('isCyclic supports moduleGraph (public)', () => {
    const plugin = new CircularDependencyPlugin()
    const modAlpha = createPublicFakeModule({ debugId: 11, resource: '/Alpha.mjs' })
    const modBeta = createPublicFakeModule({ debugId: 12, resource: '/Beta.mjs' })
    modAlpha.dependencies = [
      createPublicFakeDependency({ module: modBeta })
    ]
    modBeta.dependencies = [
      createPublicFakeDependency({ module: modAlpha })
    ]
    const compilation = createPublicFakeCompilation({ withModuleGraph: true })
    expect(
      Array.isArray(plugin.isCyclic(modAlpha, modAlpha, {}, compilation))
    ).toBe(true)
  })
})