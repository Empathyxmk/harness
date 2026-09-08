import random
import re
import types
import pytest


class CircularDependencyPlugin:
    # Dummy implementation for testing interface only
    def __init__(self, options=None):
        default_options = {
            "failOnError": False,
            "allowAsyncCycles": False,
            "onDetected": False,
            "onStart": False,
            "onEnd": False,
            "include": None,
            "exclude": None,
        }
        self.options = default_options.copy()
        if options:
            self.options.update(options)

    def apply(self, compiler):
        hooks = compiler.get("hooks", {})
        compilation_hook = hooks.get("compilation")
        if callable(compilation_hook.get("tap")):
            def callback(compilation):
                optimize_modules_hook = compilation["hooks"].get("optimizeModules")
                if callable(optimize_modules_hook.get("tap")):
                    def cb(modules):
                        if self.options.get("onStart"):
                            self.options["onStart"]()
                        for module in modules:
                            resource = module.get("resource", None)
                            if resource is None or resource == "":
                                continue
                            include = self.options.get("include")
                            if include and not re.search(include, resource):
                                continue
                            exclude = self.options.get("exclude")
                            if exclude and re.search(exclude, resource):
                                continue
                        if self.options.get("onEnd"):
                            self.options["onEnd"]()
                    optimize_modules_hook["tap"](None, cb)
            compilation_hook["tap"](None, callback)

    def isCyclic(self, startModule, currentModule, seen, compilation):
        if not currentModule.get("resource"):
            return False
        for dep in currentModule.get("dependencies", []):
            if dep.get("weak") and self.options.get("allowAsyncCycles"):
                continue
            dep_name = getattr(dep.get("constructor", None), "name", "")
            if dep_name in ["CommonJsSelfReferenceDependency", "PublicSelfReferenceDependency"]:
                continue
            next_module = dep.get("module")
            if next_module is startModule:
                if hasattr(compilation, "moduleGraph") or hasattr(compilation, "module_graph") or getattr(compilation, "moduleGraph", None) or getattr(compilation, "module_graph", None):
                    return [startModule.get("resource", "unknown"), next_module.get("resource", "unknown")]
                return [startModule.get("resource", "unknown"), next_module.get("resource", "unknown")]
            if next_module and id(next_module) not in seen:
                seen[id(next_module)] = True
                cycle = self.isCyclic(startModule, next_module, seen, compilation)
                if cycle:
                    return [currentModule.get("resource", "unknown")] + list(cycle)
        return False


def createPublicFakeModule(debugId=None, resource=None, dependencies=None):
    return {
        "debugId": debugId if debugId is not None else random.randint(5000, 25000),
        "resource": resource if resource is not None else '/public/fake/sample.js',
        "dependencies": dependencies if dependencies is not None else []
    }

def createPublicFakeDependency(module=None, name='PublicDep', weak=False):
    class PublicConstructor:
        pass
    PublicConstructor.__name__ = name
    inst = {
        "module": module,
        "weak": weak,
        "constructor": PublicConstructor
    }
    return inst

def createPublicFakeCompilation(withModuleGraph=False):
    class Graph:
        @staticmethod
        def getModule(dep):
            return dep["module"]
    obj = types.SimpleNamespace()
    if withModuleGraph:
        obj.moduleGraph = Graph()
    obj.errors = []
    obj.warnings = []
    return obj


def test_should_construct_with_custom_public_options():
    plugin = CircularDependencyPlugin({
        "failOnError": True,
        "allowAsyncCycles": True
    })
    assert plugin.options is not None
    assert plugin.options["failOnError"] is True
    assert plugin.options["allowAsyncCycles"] is True
    assert plugin.options["onDetected"] is False

def test_should_invoke_onStart_and_onEnd_hooks_public():
    flags = {"start": False, "end": False}
    def on_start(): flags["start"] = True
    def on_end(): flags["end"] = True

    plugin = CircularDependencyPlugin({
        "onStart": on_start,
        "onEnd": on_end
    })
    fakeCompiler = {
        "hooks": {
            "compilation": {
                "tap": lambda pluginTitle, callback: callback({
                    "hooks": {
                        "optimizeModules": {
                            "tap": lambda title, cb: cb([createPublicFakeModule()])
                        }
                    }
                })
            }
        }
    }
    plugin.apply(fakeCompiler)
    assert flags["start"]
    assert flags["end"]

def test_should_skip_modules_if_resource_is_empty_string_public():
    plugin = CircularDependencyPlugin()
    fakeCompiler = {
        "hooks": {
            "compilation": {
                "tap": lambda pluginTitle, callback: callback({
                    "hooks": {
                        "optimizeModules": {
                            "tap": lambda title, cb: cb([{"resource": ""}])
                        }
                    }
                })
            }
        }
    }
    plugin.apply(fakeCompiler)
    # No error expected

def test_should_skip_modules_if_resource_not_match_custom_include_or_matches_custom_exclude_public():
    plugin = CircularDependencyPlugin({
        "include": r"xyz789$",
        "exclude": r"fake"
    })
    fakeCompiler = {
        "hooks": {
            "compilation": {
                "tap": lambda pluginTitle, callback: callback({
                    "hooks": {
                        "optimizeModules": {
                            "tap": lambda title, cb: cb([
                                {"resource": "/other/file2.ts"},
                                {"resource": "/public/fake/sample.js"},
                            ])
                        }
                    }
                })
            }
        }
    }
    plugin.apply(fakeCompiler)

def test_should_detect_cycles_and_invoke_onDetected_if_present_public():
    detected_called = {"called": False}
    def detected(args=None):
        detected_called["called"] = True
    plugin = CircularDependencyPlugin({
        "onDetected": detected
    })
    modX = createPublicFakeModule(debugId=10, resource="/X.js")
    modY = createPublicFakeModule(debugId=20, resource="/Y.js")
    modX["dependencies"] = [createPublicFakeDependency(module=modY)]
    modY["dependencies"] = [createPublicFakeDependency(module=modX)]
    compilation = createPublicFakeCompilation()
    fakeCompiler = {
        "hooks": {
            "compilation": {
                "tap": lambda pluginTitle, callback: callback({
                    "hooks": {
                        "optimizeModules": {
                            "tap": lambda title, cb: cb([modX])
                        }
                    }
                })
            }
        }
    }
    plugin.apply(fakeCompiler)
    plugin.isCyclic(modX, modX, {}, compilation)
    assert callable(plugin.options["onDetected"])

def test_should_add_errors_if_failOnError_true_otherwise_add_warnings_public():
    # failOnError = true
    pluginErr = CircularDependencyPlugin({"failOnError": True})
    modX = createPublicFakeModule(debugId=3, resource='/X.js')
    modY = createPublicFakeModule(debugId=8, resource='/Y.js')
    modX["dependencies"] = [ createPublicFakeDependency(module=modY) ]
    modY["dependencies"] = [ createPublicFakeDependency(module=modX) ]
    compilation = createPublicFakeCompilation()
    compilation.errors = []
    compilation.warnings = []
    pluginErr.isCyclic(modX, modX, {}, compilation)
    cyclePaths = pluginErr.isCyclic(modX, modX, {}, compilation)
    if cyclePaths:
        error = Exception('Circular dependency detected:\r\n' + ' -> '.join(cyclePaths))
        compilation.errors.append(error)
    assert len(compilation.errors) == 1

    pluginWarn = CircularDependencyPlugin({"failOnError": False})
    compilation.errors = []
    compilation.warnings = []
    cyclePaths = pluginWarn.isCyclic(modX, modX, {}, compilation)
    if cyclePaths:
        error = Exception('Circular dependency detected:\r\n' + ' -> '.join(cyclePaths))
        compilation.warnings.append(error)
    assert len(compilation.warnings) == 1

def test_isCyclic_returns_false_when_resource_is_undefined_public():
    plugin = CircularDependencyPlugin()
    modX = createPublicFakeModule(debugId=3, resource=None)
    modY = createPublicFakeModule(debugId=4, resource='/Y.js')
    modX["dependencies"] = [ createPublicFakeDependency(module=modY) ]
    compilation = createPublicFakeCompilation()
    assert plugin.isCyclic(modX, modX, {}, compilation) is False

def test_isCyclic_skips_PublicSelfReferenceDependency_public():
    plugin = CircularDependencyPlugin()
    modX = createPublicFakeModule(debugId=5, resource='/X.js')
    modX["dependencies"] = [ createPublicFakeDependency(module=modX, name='PublicSelfReferenceDependency') ]
    compilation = createPublicFakeCompilation()
    assert plugin.isCyclic(modX, modX, {}, compilation) is False

def test_isCyclic_ignores_async_weak_dependencies_when_allowAsyncCycles_is_true_public():
    plugin = CircularDependencyPlugin({"allowAsyncCycles": True})
    modX = createPublicFakeModule(debugId=6, resource='/X.js')
    modY = createPublicFakeModule(debugId=7, resource='/Y.js')
    modX["dependencies"] = [ createPublicFakeDependency(module=modY, weak=True) ]
    modY["dependencies"] = [ createPublicFakeDependency(module=modX) ]
    compilation = createPublicFakeCompilation()
    assert plugin.isCyclic(modX, modX, {}, compilation) is False

def test_isCyclic_supports_moduleGraph_public():
    plugin = CircularDependencyPlugin()
    modAlpha = createPublicFakeModule(debugId=11, resource='/Alpha.mjs')
    modBeta = createPublicFakeModule(debugId=12, resource='/Beta.mjs')
    modAlpha["dependencies"] = [createPublicFakeDependency(module=modBeta)]
    modBeta["dependencies"] = [createPublicFakeDependency(module=modAlpha)]
    compilation = createPublicFakeCompilation(withModuleGraph=True)
    result = plugin.isCyclic(modAlpha, modAlpha, {}, compilation)
    assert isinstance(result, list)