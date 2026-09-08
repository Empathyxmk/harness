#include <gtest/gtest.h>
#include "mammoth/documents.h"
#include "mammoth/docx/xmlparser.h"
#include "mammoth/docx/document_xml.h"
#include "mammoth/docx/body_xml.h"
#include "test_util/testing.h"

TEST(DocumentXmlTests, WhenBodyElementIsPresentThenBodyIsRead) {
    // ... translate setup and asserts literally ...
}

TEST(DocumentXmlTests, WhenBodyElementIsNotPresentThenErrorIsRaised) {
    // ... using ASSERT_THROW or try/catch, check for exception and string equality ...
}

TEST(DocumentXmlTests, FootnotesOfDocumentAreRead) {
    // ... full test logic as Python ...
}