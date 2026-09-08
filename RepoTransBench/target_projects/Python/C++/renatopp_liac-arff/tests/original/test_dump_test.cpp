#include <gtest/gtest.h>
#include <sstream>
#include <string>
#include "arff_cpp.h"

TEST(DumpTest, test_simple) {
    ARFFObject obj = ...; // Set OBJ as in the Python test
    std::string expected = "% XOR Dataset\n@RELATION XOR\n\n@ATTRIBUTE input1 REAL\n@ATTRIBUTE input2 REAL\n@ATTRIBUTE y REAL\n\n@DATA\n0.0,0.0,0.0\n0.0,1.0,1.0\n1.0,0.0,1.0\n1.0,1.0,0.0\n";

    std::stringstream ss;
    dump(obj, ss);
    EXPECT_EQ(ss.str(), expected);
}