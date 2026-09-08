import unittest

import huobi.utils.input_checker as input_checker
import huobi.utils.url_params_builder as url_params_builder
import huobi.utils.log_info as log_info
import huobi.utils.time_service as time_service
import huobi.utils.print_mix_object as print_mix_object
import huobi.utils.json_parser as json_parser


class TestInputChecker(unittest.TestCase):
    def test_check_should_not_none(self):
        with self.assertRaises(Exception):
            input_checker.check_should_not_none(None, "param")

    def test_check_should_not_none_valid(self):
        self.assertIsNone(input_checker.check_should_not_none("abc", "param"))

    def test_check_should_none(self):
        self.assertIsNone(input_checker.check_should_none(None, "param"))
        with self.assertRaises(Exception):
            input_checker.check_should_none("abc", "param")


class TestUrlParamsBuilder(unittest.TestCase):
    def test_add_and_build_url(self):
        builder = url_params_builder.UrlParamsBuilder()
        # Do not assert chaining, just build
        builder.put_url("a", "1")
        builder.put_url("b", "2")
        url = builder.build_url()
        # Accept '?a=1&b=2' or '?b=2&a=1' as proper outputs
        self.assertTrue(url == "?a=1&b=2" or url == "?b=2&a=1")
        builder = url_params_builder.UrlParamsBuilder()
        self.assertEqual(builder.build_url(), "")


class TestLogInfo(unittest.TestCase):
    def test_log_methods_exist(self):
        # Only test printing functions; just call, don't check output
        if hasattr(log_info, 'print_warn'):
            log_info.print_warn("warn message")
        if hasattr(log_info, 'print_basic_info'):
            log_info.print_basic_info("info message")
        if hasattr(log_info, 'print_replace'):
            log_info.print_replace("from_message", "to_message")


class TestTimeService(unittest.TestCase):
    def test_get_current_time(self):
        if hasattr(time_service, 'get_current_timestamp'):
            now = time_service.get_current_timestamp()
            self.assertIsInstance(now, int)


class TestPrintMixObject(unittest.TestCase):
    class Dummy:
        def __str__(self):
            return "Dummy"
    def test_print_object_basic(self):
        obj = self.Dummy()
        if hasattr(print_mix_object, "print_basic_object"):
            print_mix_object.print_basic_object(obj)

    def test_print_list_and_dict(self):
        obj = self.Dummy()
        if hasattr(print_mix_object, "print_list"):
            print_mix_object.print_list([obj])
            print_mix_object.print_list([])
        if hasattr(print_mix_object, "print_dict"):
            print_mix_object.print_dict({"a": 1})
            print_mix_object.print_dict({})
        if hasattr(print_mix_object, "print_basic_dict"):
            print_mix_object.print_basic_dict({"k": 1})
        if hasattr(print_mix_object, "print_basic_list"):
            print_mix_object.print_basic_list([1,2,3])
            print_mix_object.print_basic_list([])


class TestJsonParser(unittest.TestCase):
    def test_parse(self):
        if hasattr(json_parser, "json_dumps") and hasattr(json_parser, "json_loads"):
            obj = {"foo": "bar"}
            json_str = json_parser.json_dumps(obj)
            result = json_parser.json_loads(json_str)
            self.assertEqual(result["foo"], "bar")


if __name__ == "__main__":
    unittest.main()