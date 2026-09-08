#include <gtest/gtest.h>
#include "pyzbar/scripts/read_zbar.h"
#include <fstream>
#include <sstream>
#include <string>

class ReadZbarTest : public ::testing::Test {};

TEST_F(ReadZbarTest, ReadQRCode) {
    std::stringstream buffer;
    std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());

    read_zbar_main({"tests/original/qrcode.png"}); // Provide path to test image
    std::cout.rdbuf(old);

    std::string line = buffer.str();
    EXPECT_TRUE(!line.empty());
    // Platform encoding: check for "Thalassiodracon" or b'Thalassiodracon'
    EXPECT_TRUE(line.find("Thalassiodracon") != std::string::npos);
}

TEST_F(ReadZbarTest, ReadCode128) {
    std::stringstream buffer;
    std::streambuf* old = std::cout.rdbuf(buffer.rdbuf());

    read_zbar_main({"tests/original/code128.png"}); // Provide path to test image
    std::cout.rdbuf(old);

    std::string results = buffer.str();
    EXPECT_TRUE(!results.empty());
    EXPECT_TRUE(results.find("Foramenifera") != std::string::npos);
    EXPECT_TRUE(results.find("Rana temporaria") != std::string::npos);
}