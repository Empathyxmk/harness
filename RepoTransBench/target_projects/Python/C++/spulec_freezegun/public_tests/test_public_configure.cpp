#include <gtest/gtest.h>
#include <string>

TEST(PublicConfigureTest, ConfigureEnvVar) {
    std::string key = "PUBLIC_FG_TEST_ENVVAR";
    setenv(key.c_str(), "enabled", 1);
    ASSERT_EQ(std::string(getenv(key.c_str())), "enabled");
    unsetenv(key.c_str());
    ASSERT_EQ(getenv(key.c_str()), nullptr);
}

TEST(PublicConfigureTest, SetAttrReversibility) {
    struct Dummy { int foo; };
    Dummy d;
    d.foo = 77;
    ASSERT_EQ(d.foo, 77);
}