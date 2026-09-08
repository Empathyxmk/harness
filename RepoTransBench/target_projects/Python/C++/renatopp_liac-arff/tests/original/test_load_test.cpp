#include <gtest/gtest.h>
#include <sstream>
#include <string>
#include "arff_cpp.h"

TEST(LoadTest, test_simple) {
    std::string arff = "% XOR Dataset\n@RELATION XOR\n\n@ATTRIBUTE input1 REAL\n@ATTRIBUTE input2 REAL\n@ATTRIBUTE y REAL\n\n@DATA\n0.0,0.0,0.0\n0.0,1.0,1.0\n1.0,0.0,1.0\n1.0,1.0,0.0\n% \n% \n% ";
    std::istringstream file(arff);
    ARFFObject obj = load(file);

    EXPECT_EQ(obj.description, "XOR Dataset");
    EXPECT_EQ(obj.relation, "XOR");
    EXPECT_EQ(obj.attributes[0].name, "input1");
    EXPECT_EQ(obj.attributes[0].type, "REAL");
    ASSERT_EQ(obj.data_dense[0][0], 0.0);
    ASSERT_EQ(obj.data_dense[0][1], 0.0);
    ASSERT_EQ(obj.data_dense[0][2], 0.0);
}