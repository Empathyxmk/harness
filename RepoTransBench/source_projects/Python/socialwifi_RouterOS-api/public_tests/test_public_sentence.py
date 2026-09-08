from unittest import TestCase

from routeros_api import exceptions
from routeros_api import sentence


class TestResponseSentencePublic(TestCase):
    def test_done(self):
        response = sentence.ResponseSentence.parse([b'!done', b'.tag=d'])
        self.assertEqual(response.type, b'done')

    def test_simple_re(self):
        response = sentence.ResponseSentence.parse([b'!re', b'.tag=r'])
        self.assertEqual(response.type, b're')

    def test_re_with_attributes(self):
        response = sentence.ResponseSentence.parse([b'!re', b'=c=d'])
        self.assertEqual(response.attributes[b'c'], b'd')

    def test_re_with_tag(self):
        response = sentence.ResponseSentence.parse([b'!re', b'.tag=x'])
        self.assertEqual(response.tag, b'x')

    def test_re_with_invalid_word(self):
        self.assertRaises(exceptions.RouterOsApiParsingError,
                          sentence.ResponseSentence.parse, [b'!re', b'-tag=x'])

    def test_trap(self):
        response = sentence.ResponseSentence.parse([b'!trap', b'=message=z'])
        self.assertEqual(response.type, b'trap')
        self.assertEqual(response.attributes[b'message'], b'z')


class TestCommandSentencePublic(TestCase):
    def test_login_sentence(self):
        command = sentence.CommandSentence(b'/api', b'connect')
        command.set(b'user', b'admin2')
        self.assertEqual(command.get_api_format(),
                         [b'/api/connect', b'=user=admin2'])

    def test_query_sentence(self):
        command = sentence.CommandSentence(b'/ip/address/', b'print')
        command.filter(address=b'10.1.1.1')
        self.assertEqual(command.get_api_format(),
                         [b'/ip/address/print', b'?address=10.1.1.1'])

    def test_query_sentence_with_tag(self):
        command = sentence.CommandSentence(b'/ip/address/', b'print', tag=b'7')
        command.filter(address=b'10.1.1.1')
        self.assertEqual(command.get_api_format(),
                         [b'/ip/address/print', b'?address=10.1.1.1', b'.tag=7'])