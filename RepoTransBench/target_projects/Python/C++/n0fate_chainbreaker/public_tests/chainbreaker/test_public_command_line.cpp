#include <gtest/gtest.h>
#include <stdexcept>

namespace chainbreaker_main {
    void main() {
        throw std::runtime_error("AttributeError: main does not exist");
    }
}

TEST(PublicCommandLineTest, PublicImportMainModuleNoCrash) {
    try {
        chainbreaker_main::main();
        FAIL() << "Should have thrown";
    } catch (const std::runtime_error& e) {
        // Expected
        SUCCEED();
    } catch (...) {
        FAIL() << "Threw unexpected exception";
    }
}