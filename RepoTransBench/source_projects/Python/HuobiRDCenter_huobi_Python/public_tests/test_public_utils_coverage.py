import unittest

import huobi.utils.input_checker as input_checker
import huobi.utils.url_params_builder as url_params_builder
import huobi.utils.log_info as log_info
import huobi.utils.time_service as time_service
import huobi.utils.print_mix_object as print_mix_object
import huobi.utils.json_parser as json_parser


class TestInputCheckerPublic(unittest.TestCase):
    def test_check_should_not_none(self):
        with self.assertRaises(Exception):
            input_checker.check_should_not_none(None, "different_param")

    def test_check_should_not_none_valid(self):
        self.assertIsNone(input_checker.check_should_not_none(123, "another_param"))

    def test_check_should_none(self):
        self.assertIsNone(input_checker.check_should_none(None, "wonka_param"))
        with self.assertRaises(Exception):
            input_checker.check_should_none(0, "wonka_param")


class TestUrlParamsBuilderPublic(unittest.TestCase):
    def test_add_and_build_url(self):
        builder = url_params_builder.UrlParamsBuilder()
        # Put different keys/values for public case
        builder.put_url("x", "alpha")
        builder.put_url("y", "beta")
        url = builder.build_url()
        # Accept '?x=alpha&y=beta' or '?y=beta&x=alpha'
        self.assertTrue(url == "?x=alpha&y=beta" or url == "?y=beta&x=alpha")
        builder = url_params_builder.UrlParamsBuilder()
        self.assertEqual(builder.build_url(), "")


class TestLogInfoPublic(unittest.TestCase):
    def test_log_methods_exist(self):
        # Only test printing functions; just call, don't check output
        if hasattr(log_info, 'print_warn'):
            log_info.print_warn("public warn message")
        if hasattr(log_info, 'print_basic_info'):
            log_info.print_basic_info("public info message")
        if hasattr(log_info, 'print_replace'):
            log_info.print_replace("public_from", "public_to")

class TestTimeServicePublic(unittest.TestCase):
    def test_get_current_time(self):
        if hasattr(time_service, 'get_current_timestamp'):
            now = time_service.get_current_timestamp()
            self.assertIsInstance(now, int)
            self.assertGreaterEqual(now, 0)

class TestPrintMixObjectPublic(unittest.TestCase):
    class Dummy:
        def __str__(self):
            return "OtherDummy"
    def test_print_object_basic(self):
        obj = self.Dummy()
        if hasattr(print_mix_object, "print_basic_object"):
            print_mix_object.print_basic_object(obj)

    def test_print_list_and_dict(self):
        obj = self.Dummy()
        if hasattr(print_mix_object, "print_list"):
            print_mix_object.print_list([obj, obj])
            print_mix_object.print_list([obj])
        if hasattr(print_mix_object, "print_dict"):
            print_mix_object.print_dict({"b": 2})
            print_mix_object.print_dict({"a": 42})
        if hasattr(print_mix_object, "print_basic_dict"):
            print_mix_object.print_basic_dict({"z": 789})
        if hasattr(print_mix_object, "print_basic_list"):
            print_mix_object.print_basic_list([9,8,7])
            print_mix_object.print_basic_list([0])

class TestJsonParserPublic(unittest.TestCase):
    def test_parse(self):
        if hasattr(json_parser, "json_dumps") and hasattr(json_parser, "json_loads"):
            obj = {"spam": "eggs"}
            json_str = json_parser.json_dumps(obj)
            result = json_parser.json_loads(json_str)
            self.assertEqual(result["spam"], "eggs")

if __name__ == "__main__":
    unittest.main()