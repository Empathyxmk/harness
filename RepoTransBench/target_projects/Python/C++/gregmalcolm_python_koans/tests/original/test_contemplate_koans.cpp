#include "gtest/gtest.h"
#include "lib/contemplate_koans.h"

TEST(TestContemplateKoans, Python2Message) {
    set_python_version(2,7);
    std::string out = reload_contemplate_koans();
    EXPECT_TRUE(out.find("Python 3 version") != std::string::npos || out.find("Try:") != std::string::npos);
}

TEST(TestContemplateKoans, Python36Warning) {
    set_python_version(3,6);
    std::string out = reload_contemplate_koans();
    EXPECT_NE(out.find("WARNING"), std::string::npos);
    EXPECT_NE(out.find("Python 3.7 or greater"), std::string::npos);
}

TEST(TestContemplateKoans, MainImport) {
    set_python_version(3,7);
    bool mountainCalled = false;
    set_dummy_mountain([&](){ mountainCalled=true; });
    reload_contemplate_koans();
    EXPECT_TRUE(mountainCalled);
}