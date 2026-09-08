#include <gtest/gtest.h>
#include <map>
#include <string>
#include <fstream>
#include <filesystem>

// Fake config with minimal key-value storage in-memory for the test
class Config {
    std::map<std::string, std::map<std::string, std::string>> data;
public:
    std::string get(const std::string& section, const std::string& option, const std::string& _default="") {
        if (data.count(section) && data[section].count(option))
            return data[section][option];
        return _default;
    }
    void set(const std::string& section, const std::string& option, const std::string& value) {
        data[section][option] = value;
    }
};

// Just to mimic config location in a temporary folder using filesystem
namespace fs = std::filesystem;

TEST(PublicConfigTest, PublicConfigGetSet) {
    Config conf;
    // Use different section/option than original tests
    ASSERT_EQ(conf.get("publicsection", "optionnotset", "some_public_default"), "some_public_default");

    conf.set("publicsection", "publicopt", "vvvtest");
    ASSERT_EQ(conf.get("publicsection", "publicopt"), "vvvtest");

    conf.set("publicsection", "publicopt", "publicvalue2");
    ASSERT_EQ(conf.get("publicsection", "publicopt"), "publicvalue2");

    // Simulate writing to 'config.ini' file
    fs::path config_path = fs::current_path() / "protontricks_config.ini";
    std::ofstream out(config_path);
    out << "[publicsection]\npublicopt=" << conf.get("publicsection", "publicopt") << "\n";
    out.close();

    // Content check
    std::ifstream in(config_path);
    std::string content((std::istreambuf_iterator<char>(in)), std::istreambuf_iterator<char>());
    ASSERT_NE(content.find("publicsection"), std::string::npos);
    ASSERT_NE(content.find("publicopt"), std::string::npos);
    ASSERT_NE(content.find("publicvalue2"), std::string::npos);
    in.close();

    // Cleanup
    fs::remove(config_path);
}