#include <gtest/gtest.h>
#include <vector>
#include <cstdio>
#include <fstream>
#include <string>
#include "src/liblda/extractdvector.h"

TEST(TestPublicExtractDVector, DummyExtractPublic) {
    std::vector<std::vector<double>> X{{5,7},{9,11}};
    std::vector<double> v = dummy_extract_dvector(X);
    ASSERT_EQ(v.size(), 2);
    EXPECT_NEAR(v[0], 7.0, 1e-8);
    EXPECT_NEAR(v[1], 9.0, 1e-8);
}

TEST(TestPublicExtractDVector, MainUsagePublic) {
    std::vector<std::string> args = {"extractdvector.py"};
    int ret = extractdvector_main(args);
    EXPECT_EQ(ret, 1);
}

TEST(TestPublicExtractDVector, MainOKPublic) {
    char fname[L_tmpnam];
    std::tmpnam(fname);
    std::vector<std::string> args = {"extractdvector.py", "dummy_in", fname};
    int ret = extractdvector_main(args);
    EXPECT_EQ(ret, 0);
    std::ifstream in(fname, std::ios::binary);
    ASSERT_TRUE(in);
    double arr[2];
    in.read(reinterpret_cast<char*>(arr), sizeof(arr));
    in.close();
    // always [2, 3] regardless of input
    EXPECT_NEAR(arr[0], 2.0, 1e-8);
    EXPECT_NEAR(arr[1], 3.0, 1e-8);
    std::remove(fname);
}