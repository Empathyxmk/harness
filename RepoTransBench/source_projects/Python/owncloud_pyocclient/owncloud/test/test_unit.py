import unittest
import datetime
import owncloud.owncloud as oc

class TestResponseError(unittest.TestCase):
    def test_init_with_int(self):
        err = oc.ResponseError(404, "MyErr")
        self.assertEqual(err.status_code, 404)
        self.assertEqual(str(err), "MyErr error: 404")
        # Not expecting AttributeError anymore since no .res property is set

    def test_init_with_response(self):
        class FakeRes:
            status_code = 400
            content = b'resbody'
        res = FakeRes()
        err = oc.ResponseError(res, "OCS")
        self.assertEqual(err.status_code, 400)
        self.assertEqual(err.get_resource_body(), b"resbody")
        self.assertTrue(str(err).startswith("HTTP error: 400 (OCS)"))

    def test_init_with_response_strcontent(self):
        class FakeRes:
            status_code = 501
            content = 'Some string'
        res = FakeRes()
        err = oc.ResponseError(res, "Txt")
        self.assertEqual(err.status_code, 501)
        self.assertEqual(err.get_resource_body(), "Some string")
        self.assertTrue("Some string" in str(err))

    def test_repr_and_branching(self):
        rr = oc.ResponseError(401)
        self.assertEqual(str(rr), "HTTP error: 401")
        # test with no content property in response
        class FakeRes:
            status_code = 500
        err2 = oc.ResponseError(FakeRes())
        self.assertIsNone(err2.get_resource_body())
        self.assertTrue("HTTP error: 500" in str(err2))

class TestOCSResponseError(unittest.TestCase):
    def test_ocs_xml_msg(self):
        class FakeRes:
            status_code = 500
            content = b'<root><message>failmsg</message></root>'
        err = oc.OCSResponseError(FakeRes())
        self.assertTrue("failmsg" in str(err))
        self.assertEqual(err.get_resource_body(), b'<root><message>failmsg</message></root>')

    def test_ocs_xml_invalid(self):
        class FakeRes:
            status_code = 400
            content = b'not<xml'
        err = oc.OCSResponseError(FakeRes())
        self.assertTrue("OCS response error" in str(err))
        self.assertEqual(err.get_resource_body(), b'not<xml')

    def test_ocs_none(self):
        err = oc.OCSResponseError(type("Fake", (), {"status_code": None, "content": None})())
        self.assertIsNone(err.get_resource_body())

class TestShareInfo(unittest.TestCase):
    def setUp(self):
        self.info = {
            'id': "123",
            'share_type': "1",
            'permissions': "3",
            'share_with': "user1",
            'share_with_displayname': "User One",
            'stime': "1777777700",
            'expiration': "2024-12-31",
            'path': "/some.txt"
        }
        self.share = oc.ShareInfo(self.info)

    def test_getters(self):
        self.assertEqual(self.share.get_id(), 123)
        self.assertEqual(self.share.get_share_type(), 1)
        self.assertEqual(self.share.get_share_with(), 'user1')
        self.assertEqual(self.share.get_share_with_displayname(), 'User One')
        self.assertEqual(self.share.get_path(), '/some.txt')
        self.assertEqual(self.share.get_expiration(), "2024-12-31")
        self.assertTrue(isinstance(self.share.get_share_time(), datetime.datetime))

    def test_int_conversion(self):
        info = {'id': 123, 'permissions': '', 'share_type': None, 'stime': '1777777700', 'expiration': None}
        share = oc.ShareInfo(info)
        self.assertEqual(share._get_int("id"), 123)
        self.assertIsNone(share._get_int("permissions"))
        self.assertIsNone(share._get_int("share_type"))
        dt = share.get_share_time()
        self.assertTrue(isinstance(dt, datetime.datetime))

    def test_missing_attrs(self):
        share = oc.ShareInfo({})
        self.assertIsNone(share.get_share_with())
        self.assertIsNone(share.get_share_with_displayname())
        self.assertIsNone(share.get_path())

    def test_del_attrs_removed(self):
        input_info = {'id': "1", "storage": "xxx", 'mail_send': 1,
                      'item_type': "foo", 'item_source': 42, 'file_source': 15, 'parent': None, 'other': 'ok', 'stime':'1000'}
        share = oc.ShareInfo(input_info)
        share.del_attrs()
        self.assertNotIn('item_type', share.share_info)
        self.assertNotIn('parent', share.share_info)
        self.assertIn('id', share.share_info)

    def test_contains_and_getitem(self):
        share = oc.ShareInfo({'id': 99, 'foo': 'bar'})
        self.assertIn('id', share)
        self.assertEqual(share['foo'], 'bar')

class TestUtils(unittest.TestCase):
    def test_escape_unescape(self):
        p = "/a b/abc.txt"
        out = oc.escape_path(p)
        self.assertTrue("%20" in out)
        self.assertEqual(oc.unescape_path(out), p)

    def test_to_unicode_bytes(self):
        self.assertEqual(oc.to_unicode(b'abc'), "abc")
        self.assertEqual(oc.to_unicode("xyz"), "xyz")

    def test_to_bytes(self):
        self.assertEqual(oc.to_bytes("xyz"), b"xyz")
        self.assertEqual(oc.to_bytes(b"xyz"), b"xyz")

    def test_strip_trailing_slash(self):
        self.assertEqual(oc.strip_trailing_slash("foo/"), "foo")
        self.assertEqual(oc.strip_trailing_slash("/bar/"), "/bar")
        self.assertEqual(oc.strip_trailing_slash("/"), "/")
        self.assertIsNone(oc.strip_trailing_slash(None))

if __name__ == "__main__":
    unittest.main()