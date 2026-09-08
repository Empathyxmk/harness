#include <gtest/gtest.h>
#include <string>

namespace apps_mod {
    class UuslugConfig {
    public:
        std::string name;
        std::string verbose_name;
        UuslugConfig(const std::string& n, const std::string& vn)
            : name(n), verbose_name(vn) {}
    };
}

TEST(PublicTestAppsPy, test_apps_config_name_public) {
    apps_mod::UuslugConfig app_config("uuslug", "Uuslug package");
    ASSERT_EQ(app_config.name, "uuslug");
    ASSERT_TRUE(app_config.verbose_name.find("uuslug") != std::string::npos ||
                app_config.verbose_name.find("Uuslug") != std::string::npos);
}