#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

namespace uuslug_mod {
    void uuslug(const std::string& s, void* instance) {
        if (!instance) throw std::runtime_error("Not a model instance");
    }
}

TEST(PublicTestUuslugFunc, test_uuslug_raises_for_model_base_public) {
    struct Dummy {};
    Dummy d;
    EXPECT_THROW(uuslug_mod::uuslug("def", nullptr), std::exception);
}