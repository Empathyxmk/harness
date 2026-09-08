#include <gtest/gtest.h>
#include <vector>
#include <cstdio>
#include <fstream>
#include <string>
#include "src/liblda/extractdvector.h"

TEST(TestExtractDVector, DummyExtract) {
    std::vector<std::vector<double>> X{{1,2},{3,4}};
    std::vector<double> v = dummy_extract_dvector(X);
    ASSERT_EQ(v.size(), 2);
    EXPECT_NEAR(v[0], 2.0, 1e-8);
    EXPECT_NEAR(v[1], 3.0, 1e-8);
}

TEST(TestExtractDVector, MainUsage) {
    // should return 1 if args are too few
    std::vector<std::string> args = {"extractdvector.py"};
    int ret = extractdvector_main(args);
    EXPECT_EQ(ret, 1);
}

TEST(TestExtractDVector, MainOK) {
    // Should create a file with the output values [2,3]
    char fname[L_tmpnam];
    std::tmpnam(fname);
    std::vector<std::string> args = {"extractdvector.py", "dummy_in", fname};
    int ret = extractdvector_main(args);
    EXPECT_EQ(ret, 0);
    // Read and check file content: should have double[2]{2,3}
    std::ifstream in(fname, std::ios::binary);
    ASSERT_TRUE(in);
    double arr[2];
    in.read(reinterpret_cast<char*>(arr), sizeof(arr));
    in.close();
    EXPECT_NEAR(arr[0], 2.0, 1e-8);
    EXPECT_NEAR(arr[1], 3.0, 1e-8);
    std::remove(fname);
}