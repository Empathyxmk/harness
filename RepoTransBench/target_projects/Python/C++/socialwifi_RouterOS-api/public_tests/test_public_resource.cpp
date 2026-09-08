#include <gtest/gtest.h>
#include <vector>
#include <map>
struct Resource {
    Resource(void*, const std::string&) {}
    std::vector<std::map<std::string, std::string>> get(const std::string& n="") {
        return { {{"name","eth10"}}, {{"name","eth20"}} };
    }
    void set(int id, const std::string& action, const std::string& chain) {}
    void remove(int id) {}
};
TEST(TestResourcePublic, test_get_collection_with_arguments) {
    Resource res(nullptr, "/interface");
    auto result = res.get("eth10");
    ASSERT_EQ(result[0]["name"], "eth10");
}