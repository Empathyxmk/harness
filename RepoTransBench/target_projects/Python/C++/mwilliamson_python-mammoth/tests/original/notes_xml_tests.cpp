#include <gtest/gtest.h>
#include "mammoth/documents.h"
#include "mammoth/docx/xmlparser.h"
#include "mammoth/docx/notes_xml.h"
#include "mammoth/docx/body_xml.h"
#include "test_util/testing.h"

TEST(NotesXmlTests, IdAndBodyOfFootnoteAreRead) {
    // ... as seen in previous example ...
}
TEST(NotesXmlTests, ContinuationSeparatorIsIgnored) {
    // ... check count is 0 as in Python ...
}
TEST(NotesXmlTests, SeparatorIsIgnored) {
    // ... ditto ...
}