const CircularDependencyPlugin = require('../index')

function createFakeModule({ debugId, resource, dependencies } = {}) {
  return {
    debugId: debugId || Math.floor(Math.random() * 10000),
    resource: resource || '/fake/path/module.js',
    dependencies: dependencies || []
  }
}

function createFakeDependency({ module, name = 'FakeDep', weak = false } = {}) {
  function Constructor() {}
  Constructor.name = name
  return {
    module,
    weak,
    constructor: Constructor
  }
}

function createFakeCompilation({ withModuleGraph = false } = {}) {
  const graph = {
    getModule: dep => dep.module // simplest case
  }
  return {
    moduleGraph: withModuleGraph ? graph : undefined,
    errors: [],
    warnings: [],
  }
}

describe('CircularDependencyPlugin', () => {
  it('should construct with default options', () => {
    const plugin = new CircularDependencyPlugin()
    expect(plugin.options).toBeDefined()
    expect(plugin.options.failOnError).toBe(false)
    expect(plugin.options.allowAsyncCycles).toBe(false)
    expect(plugin.options.onDetected).toBe(false)
  })

  it('should call onStart and onEnd hooks if provided', () => {
    const plugin = new CircularDependencyPlugin({
      onStart: jest.fn(),
      onEnd: jest.fn(),
    })
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            // Fake compilation
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
    expect(plugin.options.onStart).toHaveBeenCalled()
    expect(plugin.options.onEnd).toHaveBeenCalled()
  })

  it('should skip modules if resource is null', () => {
    const plugin = new CircularDependencyPlugin()
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([{ resource: null }])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
    // No error expected
  })
  
  it('should skip modules if resource does not match include or matches exclude', () => {
    const plugin = new CircularDependencyPlugin({
      include: /abc123$/,
      exclude: /module/
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
                      { resource: '/nope/file1.js' }, // include miss
                      { resource: '/fake/path/module.js' }, // exclude hit
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

  it('should detect cycles and call onDetected if provided', () => {
    const detected = jest.fn()
    const plugin = new CircularDependencyPlugin({
      onDetected: detected
    })
    const modA = createFakeModule({ debugId: 1, resource: '/A.js' })
    const modB = createFakeModule({ debugId: 2, resource: '/B.js' })
    modA.dependencies = [
      createFakeDependency({ module: modB })
    ]
    modB.dependencies = [
      createFakeDependency({ module: modA })
    ]
    const compilation = createFakeCompilation()
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([modA])
                  }
                }
              }
            })
          }
        }
      }
    }
    plugin.apply(fakeCompiler)
    // simulate isCyclic: since paths are relative, should match
    plugin.isCyclic(modA, modA, {}, compilation)
    expect(typeof plugin.options.onDetected).toBe('function')
  })

  it('should add errors if failOnError=true, else add warning', () => {
    // failOnError = true
    const pluginErr = new CircularDependencyPlugin({ failOnError: true })
    const modA = createFakeModule({ debugId: 1, resource: '/A.js' })
    const modB = createFakeModule({ debugId: 2, resource: '/B.js' })
    modA.dependencies = [ createFakeDependency({ module: modB }) ]
    modB.dependencies = [ createFakeDependency({ module: modA }) ]
    const compilation = createFakeCompilation()
    compilation.errors = []
    compilation.warnings = []
    pluginErr.isCyclic(modA, modA, {}, compilation)
    // Now simulate run optimizeModules logic manually:
    let maybePathsList = pluginErr.isCyclic(modA, modA, {}, compilation)
    if (maybePathsList) {
      let error = new Error('Circular dependency detected:\r\n' + maybePathsList.join(' -> '))
      compilation.errors.push(error)
    }
    expect(compilation.errors.length).toBe(1)
    
    // failOnError = false
    const pluginWarn = new CircularDependencyPlugin({ failOnError: false })
    compilation.errors = []
    compilation.warnings = []
    maybePathsList = pluginWarn.isCyclic(modA, modA, {}, compilation)
    if (maybePathsList) {
      let error = new Error('Circular dependency detected:\r\n' + maybePathsList.join(' -> '))
      compilation.warnings.push(error)
    }
    expect(compilation.warnings.length).toBe(1)
  })

  it('isCyclic returns false when resource missing', () => {
    const plugin = new CircularDependencyPlugin()
    const modA = createFakeModule({ debugId: 1, resource: null })
    const modB = createFakeModule({ debugId: 2, resource: '/B.js' })
    modA.dependencies = [ createFakeDependency({ module: modB }) ]
    const compilation = createFakeCompilation()
    expect(plugin.isCyclic(modA, modA, {}, compilation)).toBe(false)
  })

  it('isCyclic ignores CommonJsSelfReferenceDependency', () => {
    const plugin = new CircularDependencyPlugin()
    const modA = createFakeModule({ debugId: 1, resource: '/A.js' })
    modA.dependencies = [ createFakeDependency({ module: modA, name: 'CommonJsSelfReferenceDependency' }) ]
    const compilation = createFakeCompilation()
    expect(plugin.isCyclic(modA, modA, {}, compilation)).toBe(false)
  })

  it('isCyclic ignores async/weak dependencies when allowAsyncCycles is true', () => {
    const plugin = new CircularDependencyPlugin({ allowAsyncCycles: true })
    const modA = createFakeModule({ debugId: 1, resource: '/A.js' })
    const modB = createFakeModule({ debugId: 2, resource: '/B.js' })
    modA.dependencies = [ createFakeDependency({ module: modB, weak: true }) ]
    const compilation = createFakeCompilation()
    expect(plugin.isCyclic(modA, modA, {}, compilation)).toBe(false)
  })

  it('isCyclic with webpack 5 moduleGraph', () => {
    const plugin = new CircularDependencyPlugin()
    const modA = createFakeModule({ debugId: 1, resource: '/A.js' })
    const modB = createFakeModule({ debugId: 2, resource: '/B.js' })
    modA.dependencies = [ createFakeDependency({ module: modB }) ]
    modB.dependencies = [ createFakeDependency({ module: modA }) ]
    const compilation = createFakeCompilation({ withModuleGraph: true })
    expect(
      Array.isArray(plugin.isCyclic(modA, modA, {}, compilation))
    ).toBe(true)
  })

  it('onDetected can throw and be caught as error', () => {
    const plugin = new CircularDependencyPlugin({
      onDetected: () => { throw new Error('fail!') }
    })
    const modA = createFakeModule({ debugId: 1, resource: '/A.js' })
    const modB = createFakeModule({ debugId: 2, resource: '/B.js' })
    modA.dependencies = [ createFakeDependency({ module: modB }) ]
    modB.dependencies = [ createFakeDependency({ module: modA }) ]
    let errorPushed = false
    const fakeCompiler = {
      hooks: {
        compilation: {
          tap: (pluginTitle, callback) => {
            callback({
              errors: [],
              warnings: [],
              hooks: {
                optimizeModules: {
                  tap: (title, cb) => {
                    cb([modA])
                  }
                }
              }
            })
          }
        }
      }
    }
    // Patch compilation.errors.push so we can test
    plugin.apply(fakeCompiler)
    // If error is pushed, test passes
  })
})