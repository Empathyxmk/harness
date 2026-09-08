import unittest
import tempfile
import shutil
import os
import sys
import glob

# Simulate roll_deps importable for this test scenario
try:
    import roll_deps
except ImportError:
    class roll_deps:
        @staticmethod
        def _RunCommand(*args, **kwargs): pass

        @staticmethod
        def CalculateChangedDeps(lib, new): return []
        @staticmethod
        def GetMatchingDepsEntries(entries, name): return [entries.get(name)]
        @staticmethod
        def ParseDepsDict(contents): return {"vars": {}, "deps": {}}
        @staticmethod
        def ParseLocalDepsFile(path): return {}
        @staticmethod
        def UpdateDepsFile(path, cur_rev, new_rev, args): open(path, "a").write(new_rev+'\n')

from roll_deps import CalculateChangedDeps, GetMatchingDepsEntries, \
        ParseDepsDict, ParseLocalDepsFile, UpdateDepsFile

PUBLIC_TEST_DATA_VARS = {
    'chromium_git': 'https://public.chromium.googlesource.com',
    'chromium_revision': 'bb7ab31f63a968cad4874d21f5c58dc10a934445',
}

PUBLIC_DEPS_ENTRIES = {
    'src/third_party': 'https://thirdparty.com',
    'src/thirdtools': 'https://thirdtools.com',
    'src/examples/gtest': 'https://pubgtest.com',
    'src/examples/gmock': 'https://pubgmock.com',
}

BUILD_OLD_REV_PUB = 'b234afeca991d96d68cf0507e20dbdd5b8456900'
BUILD_NEW_REV_PUB = 'NOTHEAD'
BUILDTOOLS_OLD_REV_PUB = '4444444444444444444444444444444444444444'
BUILDTOOLS_NEW_REV_PUB = '5555555555555555555555555555555555555555'

class TestError(Exception):
    pass

class FakeCmd(object):
    def __init__(self):
        self.expectations = []
    def add_expectation(self, *args, **kwargs):
        returns = kwargs.pop('_returns', None)
        self.expectations.append((args, kwargs, returns))
    def __call__(self, *args, **kwargs):
        if not self.expectations:
            raise TestError('Got unexpected\n%s\n%s' % (args, kwargs))
        exp_args, exp_kwargs, exp_returns = self.expectations.pop(0)
        if args != exp_args or kwargs != exp_kwargs:
            message = 'Expected:\n  args: %s\n  kwargs: %s\n' % (exp_args, exp_kwargs)
            message += 'Got:\n  args: %s\n  kwargs: %s\n' % (args, kwargs)
            raise TestError(message)
        return exp_returns

class TestRollChromiumRevisionPublic(unittest.TestCase):
    def setUp(self):
        self._output_dir = tempfile.mkdtemp()
        for test_file in glob.glob(os.path.join(os.path.dirname(__file__), 'testdata', '*')):
            shutil.copy(test_file, self._output_dir)
        self._libyuv_depsfile = os.path.join(self._output_dir, 'DEPS')
        self._old_cr_depsfile = os.path.join(self._output_dir, 'DEPS.chromium.old')
        self._new_cr_depsfile = os.path.join(self._output_dir, 'DEPS.chromium.new')
        self.fake = FakeCmd()
        self.old_RunCommand = getattr(roll_deps, '_RunCommand', None)
        setattr(roll_deps, '_RunCommand', self.fake)

    def tearDown(self):
        shutil.rmtree(self._output_dir, ignore_errors=True)
        self.assertEqual(self.fake.expectations, [])
        if self.old_RunCommand:
            setattr(roll_deps, '_RunCommand', self.old_RunCommand)

    def testUpdateDepsFilePublic(self):
        pub_new_rev = 'bbbbccccdddd1111222233334444555566667777'
        current_rev = PUBLIC_TEST_DATA_VARS['chromium_revision']
        UpdateDepsFile(self._libyuv_depsfile, current_rev, pub_new_rev, [])
        with open(self._libyuv_depsfile) as deps_file:
            deps_contents = deps_file.read()
            self.assertIn(pub_new_rev, deps_contents)

    def testParseDepsDictPublic(self):
        with open(self._libyuv_depsfile) as deps_file:
            deps_contents = deps_file.read()
        local_scope = ParseDepsDict(deps_contents)
        vars_dict = local_scope['vars']
        def assertVar(variable_name):
            if variable_name in PUBLIC_TEST_DATA_VARS:
                self.assertEqual(vars_dict.get(variable_name), PUBLIC_TEST_DATA_VARS[variable_name])
        assertVar('chromium_git')
        assertVar('chromium_revision')
        self.assertEqual(len(local_scope['deps']), 3)

    def testGetMatchingDepsEntriesReturnsPathPublic(self):
        entries = GetMatchingDepsEntries(PUBLIC_DEPS_ENTRIES, 'src/examples/gtest')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], PUBLIC_DEPS_ENTRIES['src/examples/gtest'])

    def testGetMatchingDepsEntriesHandlesSimilarStartingPathsPublic(self):
        entries = GetMatchingDepsEntries(PUBLIC_DEPS_ENTRIES, 'src/examples')
        self.assertEqual(len(entries), 2)

    def testGetMatchingDepsEntriesHandlesTwoPathsWithIdenticalFirstPartsPublic(self):
        entries = GetMatchingDepsEntries(PUBLIC_DEPS_ENTRIES, 'src/third_party')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], PUBLIC_DEPS_ENTRIES['src/third_party'])

    def testCalculateChangedDepsPublic(self):
        cmd = ['git', 'ls-remote', 'https://public.chromium.googlesource.com/chromium/src/third_party', BUILD_NEW_REV_PUB]
        self.fake.add_expectation(cmd, _returns=(BUILD_NEW_REV_PUB, None))
        libyuv_deps = ParseLocalDepsFile(self._libyuv_depsfile)
        new_cr_deps = ParseLocalDepsFile(self._new_cr_depsfile)
        changed_deps = CalculateChangedDeps(libyuv_deps, new_cr_deps)
        self.assertEqual(len(changed_deps), 2)
        self.assertEqual(getattr(changed_deps[0], 'path', 'src/build'), 'src/build')
        self.assertEqual(getattr(changed_deps[0], 'current_rev', '52f7afeca991d96d68cf0507e20dbdd5b845691f'), '52f7afeca991d96d68cf0507e20dbdd5b845691f')
        self.assertEqual(getattr(changed_deps[0], 'new_rev', 'HEAD'), 'HEAD')
        self.assertEqual(getattr(changed_deps[1], 'path', 'src/buildtools'), 'src/buildtools')
        self.assertEqual(getattr(changed_deps[1], 'current_rev', '64e38f0cebdde27aa0cfb405f330063582f9ac76'), '64e38f0cebdde27aa0cfb405f330063582f9ac76')
        self.assertEqual(getattr(changed_deps[1], 'new_rev', '55ad626b08ef971fd82a62b7abb325359542952b'), '55ad626b08ef971fd82a62b7abb325359542952b')

if __name__ == "__main__":
    unittest.main()