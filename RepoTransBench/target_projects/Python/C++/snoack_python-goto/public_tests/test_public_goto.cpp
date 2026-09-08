#include <gtest/gtest.h>
#include <string>
#include <type_traits>

namespace demo_goto {

struct GotoModule {
    // In C++ we represent attributes as members but it's missing by default
    bool has_goto = false;
    bool has_label = false;
    std::string __file__ = "goto_dummy.cpp";
    std::string __name__ = "goto";
};

}

TEST(PublicGoto, HasNoGotoAndLabelByDefault) {
    demo_goto::GotoModule m;
    EXPECT_FALSE(m.has_goto);
    EXPECT_FALSE(m.has_label);
}

TEST(PublicGoto, ModuleHasFileAttribute) {
    demo_goto::GotoModule m;
    EXPECT_FALSE(m.__file__.empty());
    EXPECT_TRUE(typeid(m.__file__) == typeid(std::string));
}

TEST(PublicGoto, ModuleNameIsGoto) {
    demo_goto::GotoModule m;
    EXPECT_EQ(m.__name__, "goto");
}