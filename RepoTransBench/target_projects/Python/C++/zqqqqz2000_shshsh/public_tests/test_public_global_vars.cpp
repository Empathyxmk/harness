#include <gtest/gtest.h>
#include <unordered_map>
#include <string>

namespace shshsh {
namespace global_vars {
static std::unordered_map<std::string, std::string> vars;

void set_var(const std::string& key, const std::string& value) {
    vars[key] = value;
}
std::string get_var(const std::string& key) {
    auto it = vars.find(key);
    return (it != vars.end()) ? it->second : "";
}
void clear_var(const std::string& key) {
    vars.erase(key);
}
void clear_all() { vars.clear(); }
} // namespace global_vars
} // namespace shshsh

using namespace shshsh::global_vars;

class PublicGlobalVarsTest : public ::testing::Test {
    void SetUp() override { clear_all(); }
};

TEST_F(PublicGlobalVarsTest, SetAndGet) {
    set_var("FOO", "bar");
    ASSERT_EQ(get_var("FOO"), "bar");
    clear_var("FOO");
    ASSERT_EQ(get_var("FOO"), "");
}