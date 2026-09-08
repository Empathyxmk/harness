#include <gtest/gtest.h>
#include "injector.h"
#include <string>

using namespace injector_ns;

TEST(PublicInjectorInitTest, ReprAndModule) {
    Injector inj;
    std::string s = inj.repr();
    ASSERT_NE(s.find("Injector"), std::string::npos);
    ASSERT_TRUE(s.find("injector") != std::string::npos || s.find("Injector") != std::string::npos);
}

TEST(PublicInjectorInitTest, ConfigurationType) {
    class MyModule : public Module {
    public:
        void configure(Injector& binder) const override {
            // Nothing to configure for this test
        }
    };
    MyModule mod;
    Injector inj(mod);
    ASSERT_TRUE(typeid(inj) == typeid(Injector));
}