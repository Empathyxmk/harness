#include <gtest/gtest.h>
#include <string>
#include "mailmerge.h"

class Issue58SpacesTest : public ::testing::Test {
protected:
    std::string path;

    void SetUp() override {
        path = std::string(TEST_DATA_DIR);
    }
};

TEST_F(Issue58SpacesTest, Spaces) {
    MailMerge document(path + "/test_spaces.docx");
    std::set<std::string> expected_fields = {
        "Singleword",
        "Hello world",
        "More than one space"
    };
    EXPECT_EQ(document.get_merge_fields(), expected_fields);
}