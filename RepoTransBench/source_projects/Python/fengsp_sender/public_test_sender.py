import sys
import unittest

from sender import Mail, Message, Attachment
from sender import SenderError


class PublicBaseTestCase(unittest.TestCase):
    def setup(self):
        pass

    def teardown(self):
        pass

    def setUp(self):
        self.setup()

    def tearDown(self):
        unittest.TestCase.tearDown(self)
        self.teardown()

    def assert_equal(self, first, second):
        return self.assertEqual(first, second)

    def assert_true(self, expr, msg=None):
        self.assertTrue(expr, msg)

    def assert_false(self, expr, msg=None):
        self.assertFalse(expr, msg)

    def assert_raises(self, exception, callable=None, *args, **kwargs):
        self.assertRaises(exception, callable, *args, **kwargs)

    def assert_in(self, first, second):
        self.assertIn(first, second)

    def assert_not_in(self, first, second):
        self.assertNotIn(first, second)

    def assert_isinstance(self, obj, cls):
        self.assertIsInstance(obj, cls)

    if sys.version_info[:2] == (2, 6):
        def assertIn(self, x, y):
            assert x in y, "%r not found in %r" % (x, y)

        def assertNotIn(self, x, y):
            assert x not in y, "%r unexpectedly in %r" % (x, y)

        def assertIsInstance(self, x, y):
            assert isinstance(x, y), "not isinstance(%r, %r)" % (x, y)


class PublicMailTestCase(PublicBaseTestCase):
    def test_global_fromaddr_alternate(self):
        # No test logic in original either, so maintain parity for coverage
        pass


class PublicMessageTestCase(PublicBaseTestCase):
    def test_subject_different(self):
        msg = Message('hello')
        self.assert_equal(msg.subject, 'hello')
        msg = Message('hello', fromaddr='user1@test.com', to='user2@test.com')
        self.assert_in(msg.subject, str(msg))

    def test_to_different(self):
        msg = Message(fromaddr='alice@site.com', to='bob@site.com')
        self.assert_equal(msg.to, set(['bob@site.com']))
        self.assert_in('bob@site.com', str(msg))
        msg = Message(to=['eve@company.com', 'mallory@company.com'])
        self.assert_equal(msg.to, set(['eve@company.com', 'mallory@company.com']))

    def test_fromaddr_different(self):
        msg = Message(fromaddr='start@host.com', to='end@host.com')
        self.assert_equal(msg.fromaddr, 'start@host.com')
        self.assert_in('start@host.com', str(msg))
        msg = Message()
        msg.fromaddr = ('Other', 'other@domain.com')
        self.assert_in('<other@domain.com>', str(msg))

    def test_cc_different(self):
        msg = Message(fromaddr='one@test.com', to='two@test.com',
                      cc='cc2@cool.com')
        self.assert_in('cc2@cool.com', str(msg))

    def test_bcc_different(self):
        msg = Message(fromaddr='one2@test.com', to='two2@test.com',
                      bcc='secret2@test.com')
        self.assert_not_in('secret2@test.com', str(msg))

    def test_reply_to_different(self):
        msg = Message(fromaddr='f1@test.com', to='f2@test.com',
                      reply_to='response@test.com')
        self.assert_equal(msg.reply_to, 'response@test.com')
        self.assert_in('response@test.com', str(msg))

    def test_process_address_different(self):
        msg = Message(fromaddr=('X\r\n', 'x\r\n@foo.com'),
                      to='y\r@foo.com', reply_to='z\n@foo.com')
        self.assert_in('<x@foo.com>', str(msg))
        self.assert_in('y@foo.com', str(msg))
        self.assert_in('z@foo.com', str(msg))

    def test_charset_different(self):
        msg = Message()
        self.assert_equal(msg.charset, 'utf-8')
        msg = Message(charset='latin-1')
        self.assert_equal(msg.charset, 'latin-1')

    def test_extra_headers_different(self):
        msg = Message(fromaddr='aaa@bbb.com', to='ccc@ddd.com',
                      extra_headers={'X-Test-Header-2': 'AnotherTest'})
        self.assert_in('X-Test-Header-2: AnotherTest', str(msg))

    def test_mail_and_rcpt_options_different(self):
        msg = Message()
        self.assert_equal(msg.mail_options, [])
        self.assert_equal(msg.rcpt_options, [])
        msg = Message(mail_options=['SOME_SPECIAL=ENABLED'])
        self.assert_equal(msg.mail_options, ['SOME_SPECIAL=ENABLED'])
        msg = Message(rcpt_options=['INFO=YES'])
        self.assert_equal(msg.rcpt_options, ['INFO=YES'])

    def test_to_addrs_different(self):
        msg = Message(to='solo@place.net')
        self.assert_equal(msg.to_addrs, set(['solo@place.net']))
        msg = Message(to='to@abc.com', cc='xyz@def.com',
                      bcc=['hidden@abc.com', 'hidden2@abc.com'])
        expected_to_addrs = set(['to@abc.com', 'xyz@def.com',
                                 'hidden@abc.com', 'hidden2@abc.com'])
        self.assert_equal(msg.to_addrs, expected_to_addrs)
        msg = Message(to='unique@x.com', cc='unique@x.com')
        self.assert_equal(msg.to_addrs, set(['unique@x.com']))

    def test_validate_different(self):
        msg = Message(fromaddr='onlyfrom@fail.com')
        self.assert_raises(SenderError, msg.validate)
        msg = Message(to='onlyto@fail.com')
        self.assert_raises(SenderError, msg.validate)
        msg = Message(subject='bad\r', fromaddr='from@bad.com',
                      to='to@bad.com')
        self.assert_raises(SenderError, msg.validate)
        msg = Message(subject='bad\n', fromaddr='from@bad.com',
                      to='to@bad.com')
        self.assert_raises(SenderError, msg.validate)

    def test_attach_different(self):
        msg = Message()
        att = Attachment('public.txt')
        atts = [Attachment('a1.pdf'), Attachment('b2.pdf')]
        msg.attach(att)
        self.assert_equal(msg.attachments, [att])
        msg.attach(atts)
        self.assert_equal(msg.attachments, [att] + atts)

    def test_attach_attachment_different(self):
        msg = Message()
        msg.attach_attachment('data.csv', 'application/csv', 'header1,header2\n1,2')
        self.assert_equal(msg.attachments[0].filename, 'data.csv')
        self.assert_equal(msg.attachments[0].content_type, 'application/csv')
        self.assert_equal(msg.attachments[0].data, 'header1,header2\n1,2')

    def test_plain_text_different(self):
        plain_text = 'Greetings!\nThis is a public test.'
        msg = Message(fromaddr='person@host.com', to='person2@host.com',
                      body=plain_text)
        self.assert_equal(msg.body, plain_text)
        self.assert_in('Greetings!', msg.body)
        self.assert_in(plain_text, str(msg))