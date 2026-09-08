import unittest
import pdf_redactor
import io

class PublicRedactorTest(unittest.TestCase):
    def test_basic_redaction(self):
        pdf_in = io.BytesIO(b"%PDF-1.4\n% Public test: secret12345 replaced\nxyz 654-32-1987 zyx\n%%EOF")
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                (r"\b654-32-1987\b", lambda m: "[REDACTED-ID]")
            ]
        )
        out = io.BytesIO()
        pdf_redactor.redactor(options, pdf_in, out)
        result = out.getvalue()
        self.assertIn(b"[REDACTED-ID]", result)

    def test_unicode_filter(self):
        # Use similar logic, different text/data
        pdf_in = io.BytesIO("%PDF-1.4\nUnusual symbol: §\nID 88-99-7766\n%%EOF".encode("utf-8"))
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                (r"\b88-99-7766\b", lambda m: "<REMOVED>")
            ]
        )
        out = io.BytesIO()
        pdf_redactor.redactor(options, pdf_in, out)
        result = out.getvalue()
        self.assertIn(b"<REMOVED>", result)

    def test_multiline_filter(self):
        pdf_in = io.BytesIO(b"%PDF-1.4\nFirstLine\nID: 222-33-4444\nSecondLine\n%%EOF")
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                (r"222-33-4444", lambda m: "*****")
            ]
        )
        out = io.BytesIO()
        pdf_redactor.redactor(options, pdf_in, out)
        result = out.getvalue()
        self.assertIn(b"*****", result)


if __name__ == '__main__':
    unittest.main()