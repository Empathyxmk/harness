import unittest
import pdf_redactor

class TestRedactorOptions(unittest.TestCase):
    def test_options_defaults(self):
        opts = pdf_redactor.RedactorOptions()
        # Test default values
        self.assertIsNone(opts.input_stream)
        self.assertIsNone(opts.output_stream)
        self.assertEqual(opts.metadata_filters, {})
        self.assertEqual(opts.xmp_filters, [])
        self.assertIsNone(opts.xmp_serializer)
        self.assertEqual(opts.content_filters, [])
        self.assertEqual(opts.content_replacement_glyphs, ['?', '#', '*', ' '])
        self.assertEqual(opts.link_filters, [])

    def test_setting_options(self):
        opts = pdf_redactor.RedactorOptions()
        opts.input_stream = "input"
        opts.output_stream = "output"
        opts.metadata_filters = {"Title": [lambda v: "NewTitle"]}
        opts.content_filters = []
        opts.link_filters = [lambda href, annotation: None]
        opts.xmp_filters = [lambda xml: None]
        opts.xmp_serializer = lambda xml: "<xml />"
        self.assertEqual(opts.input_stream, "input")
        self.assertEqual(opts.output_stream, "output")
        self.assertIsInstance(opts.metadata_filters["Title"][0], type(lambda v: v))
        self.assertIsNone(opts.link_filters[0]("href", None))
        self.assertIsNone(opts.xmp_filters[0](None))
        self.assertEqual(opts.xmp_serializer(None), "<xml />")