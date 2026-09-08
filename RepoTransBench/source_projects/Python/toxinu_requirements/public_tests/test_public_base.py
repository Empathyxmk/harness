import os
import sys
import shutil
import tempfile
from unittest import TestCase

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from requirements import Requirement
from requirements import Requirements

ORIGINAL_DIRECTORY = os.getcwd()


class RequirementsPublicTestCase(TestCase):
    def setUp(self):
        self.root_directory = tempfile.mkdtemp()
        os.chdir(self.root_directory)

        self.r = Requirements()

    def tearDown(self):
        os.chdir(ORIGINAL_DIRECTORY)
        shutil.rmtree(self.root_directory)

    def test_requirement_repr_public(self):
        r = Requirement.parse('pandas==1.3.1')
        self.assertEqual(r.__repr__(), '<Requirement: "pandas==1.3.1">')

    def test_requirement_parsing_public(self):
        line = '  pandas==1.3.1,>=1.0.0 # cheese'
        r = Requirement.parse(line)
        self.assertEqual(r.line, line)
        self.assertEqual(r.name, 'pandas')
        self.assertEqual(r.specs, [('==', '1.3.1'), ('>=', '1.0.0')])

    def test_detect_files_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')

        with open(requirements_path, 'w') as f:
            f.write('pandas==1.3.1\n')

        os.mkdir(os.path.join(self.root_directory, 'requirements'))
        tests_requirements_path = os.path.join(
            self.root_directory, 'requirements', 'tests.txt')

        with open(tests_requirements_path, 'w') as f:
            f.write('pytest==6.2.5\n')

        dependencies = self.r.dependencies
        self.assertEqual(dependencies['tests_require'], ['pytest == 6.2.5'])
        self.assertEqual(
            dependencies['install_requires'], ['pandas == 1.3.1'])
        self.assertEqual(dependencies['dependency_links'], [])

    def test_different_paths_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'reqs.txt')

        with open(requirements_path, 'w') as f:
            f.write('pandas==1.3.1\n')

        os.mkdir(os.path.join(self.root_directory, 'other-requirements'))
        tests_requirements_path = os.path.join(
            self.root_directory, 'other-requirements', 'baz.txt')

        with open(tests_requirements_path, 'w') as f:
            f.write('pytest==6.2.5\n')

        self.r.requirements_path = requirements_path
        self.r.tests_requirements_path = tests_requirements_path

        dependencies = self.r.dependencies
        self.assertEqual(dependencies['tests_require'], ['pytest == 6.2.5'])
        self.assertEqual(
            dependencies['install_requires'], ['pandas == 1.3.1'])
        self.assertEqual(dependencies['dependency_links'], [])

    def test_empty_lines_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')

        with open(requirements_path, 'w') as f:
            f.write('\n\n')
            f.write('pandas==1.3.1 #I like cheese\n')
            f.write('\n')
            f.write('numpy')

        dependencies = self.r.dependencies
        self.assertEqual(
            sorted(dependencies['install_requires']),
            sorted(['pandas == 1.3.1', 'numpy']))

    def test_comments_line_ignored_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')

        with open(requirements_path, 'w') as f:
            f.write('# numpy==python3-bar\n')
            f.write('pandas==1.3.1 #I like cheese\n')

        os.mkdir(os.path.join(self.root_directory, 'requirements'))
        tests_requirements_path = os.path.join(
            self.root_directory, 'requirements', 'tests.txt')

        with open(tests_requirements_path, 'w') as f:
            f.write('pytest==6.2.5\n')

        dependencies = self.r.dependencies
        self.assertEqual(dependencies['tests_require'], ['pytest == 6.2.5'])
        self.assertEqual(dependencies['install_requires'], ['pandas == 1.3.1'])
        self.assertEqual(dependencies['dependency_links'], [])

    def test_multi_specifiers_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')
        tests_requirements_path = os.path.join(
            self.root_directory, 'tests-extra-requirements.txt')

        with open(requirements_path, 'w') as f:
            f.write('pandas<=1.3.1,>=1.0.5')

        with open(tests_requirements_path, 'w') as f:
            f.write('pandas   <=  1.3.1 , >=1.0.5')

        self.r.tests_requirements_path = 'tests-extra-requirements.txt'

        dependencies = self.r.dependencies
        self.assertEqual(
            dependencies['install_requires'], ['pandas <= 1.3.1, >= 1.0.5'])
        self.assertEqual(
            dependencies['tests_require'], ['pandas <= 1.3.1, >= 1.0.5'])

    def test_ignore_every_private_links_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')

        with open(requirements_path, 'w') as f:
            f.write('--no-index --find-links=/tmp/otherwheel SomeOtherPkg\n')
            f.write('--find-links=/tmp/otherwheel AnotherPkg\n')
            f.write('-f /tmp/otherwheel YetAnotherPkg\n')
            f.write('--extra-index-url http://baz.qux SomePkg\n')
            f.write('-i http://baz.qux TestPkg\n')
            f.write('pandas\n')
            f.write('--index-url http://baz.qux OrphanPkg\n')

        dependencies = self.r.dependencies
        self.assertEqual(dependencies['install_requires'], ['pandas'])

    def test_ignore_arguments_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')

        with open(requirements_path, 'w') as f:
            f.write('pandas\n')
            f.write('--always-unzip AnotherPackage\n')
            f.write('-Z YetAnotherPackage\n')

        dependencies = self.r.dependencies
        self.assertEqual(dependencies['install_requires'], ['pandas'])

    def test_requirements_inception_public(self):
        requirements_path = os.path.join(
            self.root_directory, 'requirements.txt')
        requirements_path_02 = os.path.join(
            self.root_directory, 'requirements-04.txt')
        requirements_path_03 = os.path.join(
            self.root_directory, 'requirements', 'requirements-05.txt')

        os.mkdir(os.path.join(self.root_directory, 'requirements'))

        with open(requirements_path, 'w') as f:
            f.write('pandas\n')
            f.write('-r requirements-04.txt\n')

        with open(requirements_path_02, 'w') as f:
            f.write('numpy\n')
            f.write('--requirement requirements/requirements-05.txt\n')

        with open(requirements_path_03, 'w') as f:
            f.write('requests==2.25.1\n')

        dependencies = self.r.dependencies
        self.assertEqual(sorted(dependencies['install_requires']),
                         sorted(['pandas', 'numpy', 'requests == 2.25.1']))