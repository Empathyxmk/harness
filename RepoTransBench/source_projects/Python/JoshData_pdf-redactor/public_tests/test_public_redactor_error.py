import unittest
import pdf_redactor

class PublicRedactorErrorTest(unittest.TestCase):

    def test_invalid_filter_type_error(self):
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                (12345, "foo")
            ]
        )
        with self.assertRaises(Exception):
            pdf_redactor.redactor(options, b"", b"")

    def test_invalid_output_stream(self):
        # Purpose: pass a None stream to invoke an error
        options = pdf_redactor.RedactorOptions(
            content_filters=[]
        )
        with self.assertRaises(Exception):
            pdf_redactor.redactor(options, b"%PDF-1.3", None)


if __name__ == '__main__':
    unittest.main()