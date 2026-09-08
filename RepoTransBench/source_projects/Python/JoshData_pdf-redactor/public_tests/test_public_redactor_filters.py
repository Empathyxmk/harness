import unittest
import pdf_redactor
import io

class PublicRedactorFiltersTest(unittest.TestCase):

    def test_filter_callable_replacement(self):
        pdf_in = io.BytesIO(b"%PDF-1.4\nSSN 159-46-2879\n%%EOF")
        def repl(m):
            return "MASKED"
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                (r"\d{3}-\d{2}-\d{4}", repl)
            ]
        )
        out = io.BytesIO()
        pdf_redactor.redactor(options, pdf_in, out)
        self.assertIn(b"MASKED", out.getvalue())

    def test_filter_non_callable_replacement(self):
        pdf_in = io.BytesIO(b"%PDF-1.4\nName: Angela Bailey\n%%EOF")
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                ("Angela Bailey", "AnonName")
            ]
        )
        out = io.BytesIO()
        pdf_redactor.redactor(options, pdf_in, out)
        self.assertIn(b"AnonName", out.getvalue())


if __name__ == '__main__':
    unittest.main()