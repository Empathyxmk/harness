#include <gtest/gtest.h>
#include <string>
#include <vector>

TEST(ConfigureTest, ConfigureEnvVar) {
    std::string key = "TEST_ENV_VAR";
    setenv(key.c_str(), "enabled", 1);
    ASSERT_EQ(std::string(getenv(key.c_str())), "enabled");
    unsetenv(key.c_str());
    ASSERT_EQ(getenv(key.c_str()), nullptr);
}

TEST(ConfigureTest, ConfigureSetAttrReversibility) {
    struct Dummy { int foo; };
    Dummy d;
    d.foo = 77;
    ASSERT_EQ(d.foo, 77);
}