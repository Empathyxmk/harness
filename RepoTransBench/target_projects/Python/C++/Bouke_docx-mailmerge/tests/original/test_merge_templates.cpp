#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "mailmerge.h"
#include "etree_mixin.h"

class MergeListTest : public EtreeMixin, public ::testing::Test {};

TEST_F(MergeListTest, BreakPage) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with page_break"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "page_break");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, BreakCol) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with column_break"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "column_break");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, BreakTextWrapping) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with textWrapping_break"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "textWrapping_break");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, SectPage) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with nextPage_section"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "nextPage_section");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, SectCont) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with continuous_section"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "continuous_section");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, SectEvenPage) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with evenPage_section"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "evenPage_section");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, SectOddPage) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with oddPage_section"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "oddPage_section");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}

TEST_F(MergeListTest, SectCol) {
    std::string docx_path = TEST_DATA_DIR "/test_merge_templates_simple.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {"fieldname"};
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    std::vector<std::map<std::string, std::string>> data = {
        {{"fieldname", "Test with nextColumn_section"}},
        {{"fieldname", "abc"}},
        {{"fieldname", "2b v ~2b"}}
    };
    document.merge_templates(data, "nextColumn_section");

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:wpc=\"http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas\" ...full xml string here... </w:document>");
    ASSERT_TRUE(assert_equal_tree(expected_tree, get_document_body_part(document)));
}