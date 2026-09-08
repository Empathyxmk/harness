#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <string>
#include <vector>
#include <map>

using ::testing::_;
using ::testing::Return;

namespace routeros_api {
namespace resource {
struct RouterOsResource {
    std::string name;
    RouterOsResource(void*, std::string n, void*) : name(n) {}
    std::vector<std::map<std::string, std::string>> get() { return {{ {"x","y"} }}; }
    void set(const std::string&, const std::string&) {}
};
}
}

TEST(ResourceTest, test_unknown_resource_get) {
    routeros_api::resource::RouterOsResource res(nullptr, "/unknown", nullptr);
    auto result = res.get();
    ASSERT_EQ(result[0]["x"], "y");
}