from unittest.mock import patch, mock_open
from pathlib import Path
from tempfile import TemporaryDirectory

from gitignore_parser import parse_gitignore, parse_gitignore_str

from unittest import TestCase, main


class TestPublic(TestCase):
    def test_simple(self):
        matches = parse_gitignore_str(
            'build/\n'
            '*.log',
            base_dir='/example'
        )
        self.assertFalse(matches('/example/main.txt'))
        self.assertTrue(matches('/example/main.log'))
        self.assertTrue(matches('/example/dir/main.log'))
        self.assertTrue(matches('/example/build'))

    def test_simple_parse_file(self):
        with patch('builtins.open', mock_open(read_data=
                                              'dist/\n'
                                              '*.tmp')):
            matches = parse_gitignore('/project/.gitignore')
            self.assertFalse(matches('/project/app.py'))
            self.assertTrue(matches('/project/app.tmp'))
            self.assertTrue(matches('/project/sub/app.tmp'))
            self.assertTrue(matches('/project/dist'))

    def test_incomplete_filename(self):
        matches = parse_gitignore_str('app.js', base_dir='/public')
        self.assertTrue(matches('/public/app.js'))
        self.assertFalse(matches('/public/test.js'))
        self.assertFalse(matches('/public/app.jsx'))
        self.assertTrue(matches('/public/dir/app.js'))
        self.assertFalse(matches('/public/dir/test.js'))
        self.assertFalse(matches('/public/dir/app.jsx'))

    def test_wildcard(self):
        matches = parse_gitignore_str(
            'error.*',
            base_dir='/tmp'
        )
        self.assertTrue(matches('/tmp/error.txt'))
        self.assertTrue(matches('/tmp/error.bak/'))
        self.assertTrue(matches('/tmp/dir/error.txt'))
        self.assertTrue(matches('/tmp/error.'))
        self.assertFalse(matches('/tmp/error'))
        self.assertFalse(matches('/tmp/errorX'))

    def test_anchored_wildcard(self):
        matches = parse_gitignore_str(
            '/success.*',
            base_dir='/dirfoo'
        )
        self.assertTrue(matches('/dirfoo/success.txt'))
        self.assertTrue(matches('/dirfoo/success.c'))
        self.assertFalse(matches('/dirfoo/a/success.java'))

    def test_trailingspaces(self):
        matches = parse_gitignore_str(
            'ignoretailspace \n'
            'notignoredspace\\ \n'
            'almostignoredspace\\  \n'
            'almostignoredspace2 \\  \n'
            'notignoredmultiplespace\\ \\ \\ ',
            base_dir='/abc'
        )
        self.assertTrue(matches('/abc/ignoretailspace'))
        self.assertFalse(matches('/abc/ignoretailspace '))
        self.assertTrue(matches('/abc/almostignoredspace '))
        self.assertFalse(matches('/abc/almostignoredspace  '))
        self.assertFalse(matches('/abc/almostignoredspace'))
        self.assertTrue(matches('/abc/almostignoredspace2  '))
        self.assertFalse(matches('/abc/almostignoredspace2   '))
        self.assertFalse(matches('/abc/almostignoredspace2 '))
        self.assertFalse(matches('/abc/almostignoredspace2'))
        self.assertTrue(matches('/abc/notignoredspace '))
        self.assertFalse(matches('/abc/notignoredspace'))
        self.assertTrue(matches('/abc/notignoredmultiplespace   '))
        self.assertFalse(matches('/abc/notignoredmultiplespace'))

    def test_comment(self):
        matches = parse_gitignore_str(
                        'firstmatch\n'
                        '#notrealcomment\n'
                        'secondmatch\n'
                        '\\#reallyamatch',
            base_dir='/bdir'
        )
        self.assertTrue(matches('/bdir/firstmatch'))
        self.assertFalse(matches('/bdir/#notrealcomment'))
        self.assertTrue(matches('/bdir/secondmatch'))
        self.assertTrue(matches('/bdir/#reallyamatch'))

    def test_ignore_directory(self):
        matches = \
            parse_gitignore_str('cache/', base_dir='/mnt')
        self.assertTrue(matches('/mnt/cache'))
        self.assertTrue(matches('/mnt/cache/subdir'))
        self.assertTrue(matches('/mnt/cache/file.txt'))
        self.assertFalse(matches('/mnt/cachex'))
        self.assertFalse(matches('/mnt/cache_v2.py'))

    def test_ignore_directory_asterisk(self):
        matches = \
            parse_gitignore_str('output/*', base_dir='/results')
        self.assertFalse(matches('/results/output'))
        self.assertTrue(matches('/results/output/folder'))
        self.assertTrue(matches('/results/output/file.txt'))

    def test_negation(self):
        matches = parse_gitignore_str(
            '''
*.bak
!keep.bak
            ''',
            base_dir='/store'
        )
        self.assertTrue(matches('/store/junk.bak'))
        self.assertFalse(matches('/store/keep.bak'))
        self.assertTrue(matches('/store/lost.bak'))

    def test_literal_exclamation_mark(self):
        matches = parse_gitignore_str(
            '\\!saveit!', base_dir='/fs'
        )
        self.assertTrue(matches('/fs/!saveit!'))
        self.assertFalse(matches('/fs/saveit!'))
        self.assertFalse(matches('/fs/saveit'))

    def test_double_asterisks(self):
        matches = parse_gitignore_str(
            'dir/**/Final', base_dir='/abc'
        )
        self.assertTrue(matches('/abc/dir/sub/Final'))
        self.assertTrue(matches('/abc/dir/foo/Final'))
        self.assertTrue(matches('/abc/dir/Final'))
        self.assertFalse(matches('/abc/dir/Finals'))

    def test_double_asterisk_without_slashes_handled_like_single_asterisk(self):
        matches = \
            parse_gitignore_str('m/n**o/p', base_dir='/usr')
        self.assertTrue(matches('/usr/m/no/p'))
        self.assertTrue(matches('/usr/m/nko/p'))
        self.assertTrue(matches('/usr/m/nno/p'))
        self.assertTrue(matches('/usr/m/noo/p'))
        self.assertFalse(matches('/usr/m/nop'))
        self.assertFalse(matches('/usr/m/n/o/p'))
        self.assertFalse(matches('/usr/m/nn/oo/p'))
        self.assertFalse(matches('/usr/m/nn/YY/oo/p'))

    def test_more_asterisks_handled_like_single_asterisk(self):
        matches = \
            parse_gitignore_str('***z/x', base_dir='/sample')
        self.assertTrue(matches('/sample/ABCz/x'))
        self.assertFalse(matches('/sample/yyy/z/x'))
        matches = \
            parse_gitignore_str('z/x***', base_dir='/sample')
        self.assertTrue(matches('/sample/z/xABC'))
        self.assertFalse(matches('/sample/z/x/abc'))

    def test_directory_only_negation(self):
        matches = parse_gitignore_str('''
content/**
!content/**/
!.hold
!content/01_data/*
            ''',
            base_dir='/vault'
        )
        self.assertFalse(matches('/vault/content/01_data/'))
        self.assertFalse(matches('/vault/content/01_data/.hold'))
        self.assertFalse(matches('/vault/content/01_data/doc.csv'))
        self.assertFalse(matches('/vault/content/02_final/'))
        self.assertFalse(matches('/vault/content/02_final/.hold'))
        self.assertTrue(
            matches('/vault/content/02_final/summary.txt')
        )

    def test_single_asterisk(self):
        matches = parse_gitignore_str('*', base_dir='/misc')
        self.assertTrue(matches('/misc/note.txt'))
        self.assertTrue(matches('/misc/folder'))
        self.assertTrue(matches('/misc/folder-trailing/'))

    def test_supports_path_type_argument(self):
        matches = parse_gitignore_str(
            'image1\n!image2', base_dir='/photos'
        )
        self.assertTrue(matches(Path('/photos/image1')))
        self.assertFalse(matches(Path('/photos/image2')))

    def test_slash_in_range_does_not_match_dirs(self):
        matches = parse_gitignore_str(
            'pqr[S-U/]stu', base_dir='/zdir'
        )
        self.assertFalse(matches('/zdir/pqrststu'))
        self.assertTrue(matches('/zdir/pqrSstu'))
        self.assertTrue(matches('/zdir/pqrTstu'))
        self.assertTrue(matches('/zdir/pqrUstu'))
        self.assertFalse(matches('/zdir/pqr/stu'))
        self.assertFalse(matches('/zdir/pqrSTUstu'))

    def test_symlink_to_another_directory(self):
        with TemporaryDirectory() as root_dir:
            with TemporaryDirectory() as other_dir:
                matches = parse_gitignore_str('linker', base_dir=root_dir)
                import os
                os.symlink(other_dir, f"{root_dir}/linker")
                self.assertTrue(matches(f"{root_dir}/linker"))
                self.assertFalse(matches(f"{root_dir}/link"))