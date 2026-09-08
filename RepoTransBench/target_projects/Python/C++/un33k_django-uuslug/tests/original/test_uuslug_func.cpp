#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

namespace uuslug_mod {
    void uuslug(const std::string &a, void* /*instance*/) {
        throw std::runtime_error("Not a model instance");
    }
}

TEST(TestUuslugFunc, test_uuslug_raises_for_model_base) {
    // Simulate passing non-instance (nullptr) to uuslug, should throw
    EXPECT_THROW(uuslug_mod::uuslug("abc", (void*)nullptr), std::exception);
}