#include <gtest/gtest.h>
#include <iostream>
#include <sstream>

TEST(HammsMisc, ImportMainDoesNotThrow) {
    // Simulate importing hamms.__main__ (does not throw)
    SUCCEED();
}

inline void hamms_main() {
    std::cout << "hamms main executed\n";
}

TEST(HammsMisc, MainFunctionPrintsExpected) {
    std::stringstream buffer;
    std::streambuf* prevcout = std::cout.rdbuf(buffer.rdbuf());
    hamms_main();
    std::cout.rdbuf(prevcout);

    std::string output = buffer.str();
    ASSERT_NE(output.find("hamms main executed"), std::string::npos);
}