#include <gtest/gtest.h>
#include <fstream>
#include <string>
#include "arff_cpp.h"

TEST(LoadDumpTest, test_simple) {
    std::string ARFF = ...; // as per ARFF string literal in Python test
    for (int count = 0; count < 10; ++count) {
        ARFFObject obj = ARFF_loads(ARFF);
        std::string out = ARFF_dumps(obj);
        EXPECT_EQ(out, ARFF);
    }
}

TEST(LoadDumpTest, test_issue_69) {
    std::ifstream infile("tests/examples/issue69.arff");
    std::stringstream buffer;
    buffer << infile.rdbuf();
    std::string string = buffer.str();

    ARFFObject obj = ARFF_loads(string);

    for (int i = 0; i < 10; ++i) {
        ARFFObject tmp_obj = ARFF_loads(string);
        std::string tmp_string = ARFF_dumps(tmp_obj);
        ARFFObject new_obj = ARFF_loads(tmp_string);
        EXPECT_EQ(new_obj, obj);
    }
}