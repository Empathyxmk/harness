import unittest
import pdf_redactor

class PublicRedactorOptionsTest(unittest.TestCase):

    def test_metadata_defaults(self):
        options = pdf_redactor.RedactorOptions(
            metadata={
                "Title": "PublicTitle",
                "Subject": "PublicSubj",
                "Author": "AuthorPerson",
            }
        )
        self.assertEqual(options.metadata["Title"], "PublicTitle")
        self.assertEqual(options.metadata["Subject"], "PublicSubj")
        self.assertEqual(options.metadata["Author"], "AuthorPerson")

    def test_options_filters_list(self):
        options = pdf_redactor.RedactorOptions(
            content_filters=[
                (r"\d{2}-\d{2}-\d{4}", "REDACT"),
                (r"SecretWord", "VisibleWord"),
            ]
        )
        self.assertIsInstance(options.content_filters, list)
        self.assertEqual(len(options.content_filters), 2)
        self.assertEqual(options.content_filters[1][1], "VisibleWord")


if __name__ == "__main__":
    unittest.main()