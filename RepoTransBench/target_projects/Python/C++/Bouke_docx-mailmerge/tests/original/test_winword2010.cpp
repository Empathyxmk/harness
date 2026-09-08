#include <gtest/gtest.h>
#include <string>
#include "mailmerge.h"
#include "etree_mixin.h"

class Windword2010Test : public EtreeMixin, public ::testing::Test {};

TEST_F(Windword2010Test, Basic) {
    std::string docx_path = TEST_DATA_DIR "/test_winword2010.docx";
    MailMerge document(docx_path);

    std::set<std::string> expected_fields = {
        "Titel", "Voornaam", "Achternaam", "Adresregel_1", "Postcode",
        "Plaats", "Provincie", "Land_of_regio"
    };
    EXPECT_EQ(document.get_merge_fields(), expected_fields);

    document.merge({
        {"Voornaam", "Bouke"},
        {"Achternaam", "Haarsma"},
        {"Land_of_regio", "The Netherlands"},
        {"Provincie", ""},
        {"Postcode", "9723 ZA"},
        {"Plaats", "Groningen"},
        {"Adresregel_1", "Helperpark 278d\nP.O. Box"},
        {"Titel", "dhr."}
    });

    std::stringstream ss;
    document.write(ss);

    XMLNode expected_tree = XMLNode::fromString(
        "<w:document xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\" ...full xml string here...</w:document>"
    );
    ASSERT_TRUE(assert_equal_tree(expected_tree, document.get_document_root()));
    // Settings should not have a mailMerge node
    EXPECT_TRUE(document.settings_getroot_find("{w}mailMerge") == nullptr);
}