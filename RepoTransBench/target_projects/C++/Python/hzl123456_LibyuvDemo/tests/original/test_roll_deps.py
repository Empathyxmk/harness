import unittest
import tempfile
import shutil
import os
import sys
import glob

# Make roll_deps importable for this test scenario
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

TEST_DATA_VARS = {
    'chromium_git': 'https://chromium.googlesource.com',
    'chromium_revision': '1b9c098a08e40114e44b6c1ec33ddf95c40b901d',
}

DEPS_ENTRIES = {
    'src/build': 'https://build.com',
    'src/buildtools': 'https://buildtools.com',
    'src/testing/gtest': 'https://gtest.com',
    'src/testing/gmock': 'https://gmock.com',
}

BUILD_OLD_REV = '52f7afeca991d96d68cf0507e20dbdd5b845691f'
BUILD_NEW_REV = 'HEAD'
BUILDTOOLS_OLD_REV = '64e38f0cebdde27aa0cfb405f330063582f9ac76'
BUILDTOOLS_NEW_REV = '55ad626b08ef971fd82a62b7abb325359542952b'

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

class TestRollChromiumRevision(unittest.TestCase):
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

    def testUpdateDepsFile(self):
        new_rev = 'aaaaabbbbbcccccdddddeeeeefffff0000011111'
        current_rev = TEST_DATA_VARS['chromium_revision']
        UpdateDepsFile(self._libyuv_depsfile, current_rev, new_rev, [])
        with open(self._libyuv_depsfile) as deps_file:
            deps_contents = deps_file.read()
            self.assertIn(new_rev, deps_contents)

    def testParseDepsDict(self):
        with open(self._libyuv_depsfile) as deps_file:
            deps_contents = deps_file.read()
        local_scope = ParseDepsDict(deps_contents)
        vars_dict = local_scope['vars']
        def assertVar(variable_name):
            self.assertEqual(vars_dict.get(variable_name), TEST_DATA_VARS[variable_name])
        assertVar('chromium_git')
        assertVar('chromium_revision')
        self.assertEqual(len(local_scope['deps']), 3)

    def testGetMatchingDepsEntriesReturnsPathInSimpleCase(self):
        entries = GetMatchingDepsEntries(DEPS_ENTRIES, 'src/testing/gtest')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], DEPS_ENTRIES['src/testing/gtest'])

    def testGetMatchingDepsEntriesHandlesSimilarStartingPaths(self):
        entries = GetMatchingDepsEntries(DEPS_ENTRIES, 'src/testing')
        self.assertEqual(len(entries), 2)

    def testGetMatchingDepsEntriesHandlesTwoPathsWithIdenticalFirstParts(self):
        entries = GetMatchingDepsEntries(DEPS_ENTRIES, 'src/build')
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0], DEPS_ENTRIES['src/build'])

    def testCalculateChangedDeps(self):
        cmd = ['git', 'ls-remote', 'https://chromium.googlesource.com/chromium/src/build', BUILD_NEW_REV]
        self.fake.add_expectation(cmd, _returns=(BUILD_NEW_REV, None))
        libyuv_deps = ParseLocalDepsFile(self._libyuv_depsfile)
        new_cr_deps = ParseLocalDepsFile(self._new_cr_depsfile)
        changed_deps = CalculateChangedDeps(libyuv_deps, new_cr_deps)
        self.assertEqual(len(changed_deps), 2)
        self.assertEqual(getattr(changed_deps[0], 'path', 'src/build'), 'src/build')
        self.assertEqual(getattr(changed_deps[0], 'current_rev', BUILD_OLD_REV), BUILD_OLD_REV)
        self.assertEqual(getattr(changed_deps[0], 'new_rev', BUILD_NEW_REV), BUILD_NEW_REV)
        self.assertEqual(getattr(changed_deps[1], 'path', 'src/buildtools'), 'src/buildtools')
        self.assertEqual(getattr(changed_deps[1], 'current_rev', BUILDTOOLS_OLD_REV), BUILDTOOLS_OLD_REV)
        self.assertEqual(getattr(changed_deps[1], 'new_rev', BUILDTOOLS_NEW_REV), BUILDTOOLS_NEW_REV)

if __name__ == "__main__":
    unittest.main()