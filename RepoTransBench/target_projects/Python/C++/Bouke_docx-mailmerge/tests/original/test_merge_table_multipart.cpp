#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include "mailmerge.h"
#include "etree_mixin.h"

class MergeTableRowsMultipartTest : public EtreeMixin, public ::testing::Test {
protected:
    MailMerge* document;
    std::string expected_xml;
    XMLNode expected_tree;

    virtual void SetUp() override {
        std::string docx_path = TEST_DATA_DIR "/test_merge_table_multipart.docx";
        document = new MailMerge(docx_path);
        expected_xml = "<w:document xmlns:ns1=\"http://schemas.openxmlformats.org/officeDocument/2006/relationships\" xmlns:w=\"http://schemas.openxmlformats.org/wordprocessingml/2006/main\"><w:body><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00231DA5\" w:rsidRDefault=\"00DA4DE0\"><w:pPr><w:pStyle w:val=\"Ttulo\" /></w:pPr><w:r><w:t>Grades</w:t></w:r></w:p><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:r><w:t>Bouke Haarsma</w:t></w:r><w:r w:rsidR=\"002C29C5\"><w:t xml:space=\"preserve\"> </w:t></w:r><w:r w:rsidR=\"00DA4DE0\"><w:t>received the grades</w:t></w:r><w:r w:rsidR=\"002C29C5\"><w:t xml:space=\"preserve\"> for </w:t></w:r><w:r><w:t /></w:r><w:r w:rsidR=\"00DA4DE0\"><w:t xml:space=\"preserve\"> in the table below.</w:t></w:r></w:p><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"00DA4DE0\" /><w:tbl><w:tblPr><w:tblStyle w:val=\"Sombreadoclaro-nfasis1\" /><w:tblW w:type=\"auto\" w:w=\"0\" /><w:tblLook w:val=\"04E0\" /></w:tblPr><w:tblGrid><w:gridCol w:w=\"1777\" /><w:gridCol w:w=\"4894\" /><w:gridCol w:w=\"1845\" /></w:tblGrid><w:tr w:rsidR=\"00DA4DE0\" w:rsidTr=\"00C829DD\"><w:trPr><w:cnfStyle w:val=\"100000000000\" /></w:trPr><w:tc><w:tcPr><w:cnfStyle w:val=\"001000000000\" /><w:tcW w:type=\"dxa\" w:w=\"1809\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"00DA4DE0\"><w:r><w:t>Class Code</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"5529\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"00DA4DE0\"><w:pPr><w:cnfStyle w:val=\"100000000000\" /></w:pPr><w:r><w:t>Class Name</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"1178\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"00DA4DE0\"><w:pPr><w:cnfStyle w:val=\"100000000000\" /></w:pPr><w:r><w:t>Grade</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR=\"00DA4DE0\" w:rsidTr=\"00C829DD\"><w:trPr><w:cnfStyle w:val=\"000000100000\" /></w:trPr><w:tc><w:tcPr><w:cnfStyle w:val=\"001000000000\" /><w:tcW w:type=\"dxa\" w:w=\"1809\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:r><w:t>ECON101</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"5529\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"000000100000\" /></w:pPr><w:r><w:t>Economics 101</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"1178\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"000000100000\" /></w:pPr><w:r><w:t>A</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR=\"00DA4DE0\" w:rsidTr=\"00C829DD\"><w:trPr><w:cnfStyle w:val=\"000000100000\" /></w:trPr><w:tc><w:tcPr><w:cnfStyle w:val=\"001000000000\" /><w:tcW w:type=\"dxa\" w:w=\"1809\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:r><w:t>ECONADV</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"5529\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"000000100000\" /></w:pPr><w:r><w:t>Economics Advanced</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"1178\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"000000100000\" /></w:pPr><w:r><w:t>B</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR=\"00DA4DE0\" w:rsidTr=\"00C829DD\"><w:trPr><w:cnfStyle w:val=\"000000100000\" /></w:trPr><w:tc><w:tcPr><w:cnfStyle w:val=\"001000000000\" /><w:tcW w:type=\"dxa\" w:w=\"1809\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:r><w:t>OPRES</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"5529\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"000000100000\" /></w:pPr><w:r><w:t>Operations Research</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"1178\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"000000100000\" /></w:pPr><w:r><w:t>A</w:t></w:r></w:p></w:tc></w:tr><w:tr w:rsidR=\"00C829DD\" w:rsidTr=\"00C829DD\"><w:trPr><w:cnfStyle w:val=\"010000000000\" /></w:trPr><w:tc><w:tcPr><w:cnfStyle w:val=\"001000000000\" /><w:tcW w:type=\"dxa\" w:w=\"1809\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00C829DD\" w:rsidRDefault=\"00C829DD\"><w:r><w:t>THESIS</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"5529\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00C829DD\" w:rsidRDefault=\"00C829DD\"><w:pPr><w:cnfStyle w:val=\"010000000000\" /></w:pPr><w:r><w:t>Final thesis</w:t></w:r></w:p></w:tc><w:tc><w:tcPr><w:tcW w:type=\"dxa\" w:w=\"1178\" /></w:tcPr><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00C829DD\" w:rsidRDefault=\"0037127B\"><w:pPr><w:cnfStyle w:val=\"010000000000\" /></w:pPr><w:r><w:t>A</w:t></w:r></w:p></w:tc></w:tr></w:tbl><w:p w:rsidP=\"00DA4DE0\" w:rsidR=\"00DA4DE0\" w:rsidRDefault=\"00DA4DE0\" w:rsidRPr=\"00DA4DE0\"><w:bookmarkStart w:id=\"0\" w:name=\"_GoBack\" /><w:bookmarkEnd w:id=\"0\" /></w:p><w:sectPr w:rsidR=\"00DA4DE0\" w:rsidRPr=\"00DA4DE0\" w:rsidSect=\"003B4151\"><w:headerReference ns1:id=\"rId7\" w:type=\"default\" /><w:pgSz w:h=\"16840\" w:w=\"11900\" /><w:pgMar w:bottom=\"1440\" w:footer=\"708\" w:gutter=\"0\" w:header=\"708\" w:left=\"1800\" w:right=\"1800\" w:top=\"1672\" /><w:cols w:space=\"708\" /><w:docGrid w:linePitch=\"360\" /></w:sectPr></w:body></w:document>";
        expected_tree = XMLNode::fromString(expected_xml);
    }

    virtual void TearDown() override {
        document->close();
        delete document;
    }
};

TEST_F(MergeTableRowsMultipartTest, MergeRowsOnMultipartFile) {
    ASSERT_EQ(document->get_merge_fields(), (std::set<std::string>{"student_name", "study_name", "class_name", "class_code", "class_grade", "thesis_grade"}));
    document->merge({
        {"student_name", "Bouke Haarsma"},
        {"study", "Industrial Engineering and Management"},
        {"thesis_grade", "A"}
    });
    std::vector<std::map<std::string, std::string>> rows = {
        {{"class_code", "ECON101"}, {"class_name", "Economics 101"}, {"class_grade", "A"}},
        {{"class_code", "ECONADV"}, {"class_name", "Economics Advanced"}, {"class_grade", "B"}},
        {{"class_code", "OPRES"},   {"class_name", "Operations Research"}, {"class_grade", "A"}}
    };
    document->merge_rows("class_code", rows);

    std::stringstream ss;
    document->write(ss);

    // Only check document part
    for (const auto& part : document->parts()) {
        if (part.getroot().tag() == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}document") {
            ASSERT_TRUE(assert_equal_tree(expected_tree, part.getroot()));
        }
    }
}

TEST_F(MergeTableRowsMultipartTest, MergeUnifiedOnMultipartFile) {
    document->merge({
        {"student_name", "Bouke Haarsma"},
        {"study", "Industrial Engineering and Management"},
        {"thesis_grade", "A"},
        {"class_code", std::vector<std::map<std::string, std::string>>{
            {{"class_code", "ECON101"}, {"class_name", "Economics 101"}, {"class_grade", "A"}},
            {{"class_code", "ECONADV"}, {"class_name", "Economics Advanced"}, {"class_grade", "B"}},
            {{"class_code", "OPRES"},   {"class_name", "Operations Research"}, {"class_grade", "A"}}
        }}
    });

    std::stringstream ss;
    document->write(ss);

    // Only check document part
    for (const auto& part : document->parts()) {
        if (part.getroot().tag() == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}document") {
            ASSERT_TRUE(assert_equal_tree(expected_tree, part.getroot()));
        }
    }
}