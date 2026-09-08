#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "mailmerge.h"
#include "etree_mixin.h"

class MergeListTest_Pages : public EtreeMixin, public ::testing::Test {};

TEST_F(MergeListTest_Pages, Pages) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_pages.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "xyz"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_pages(data);

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>"
    );
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest_Pages, PagesWithMultiplePages) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_pages_paged.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "xyz"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_pages(data);

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>"
    );
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}