import unittest
from mailmerge import MailMerge

class TestMailMergeParseInstr(unittest.TestCase):
    def test_parse_instr_valid(self):
        instr = 'MERGEFIELD  somefield  \\* MERGEFORMAT'
        name = MailMerge._MailMerge__parse_instr(instr)
        self.assertEqual(name, 'somefield')

    def test_parse_instr_invalid(self):
        instr = 'SOMETHINGELSE testing'
        name = MailMerge._MailMerge__parse_instr(instr)
        self.assertIsNone(name)

    def test_parse_instr_quoted(self):
        instr = 'MERGEFIELD "another field"'
        name = MailMerge._MailMerge__parse_instr(instr)
        self.assertEqual(name, 'another field')