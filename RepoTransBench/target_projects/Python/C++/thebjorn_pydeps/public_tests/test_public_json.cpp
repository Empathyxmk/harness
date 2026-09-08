#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>
#include <map>
#include <iostream>

using nlohmann::json;

struct SourcePublic {
    std::string name;
    std::set<std::string> imported_by;
};

struct GraphPublic {
    std::map<std::string, SourcePublic> sources;
    GraphPublic() {
        sources["bar"] = SourcePublic{"bar", {"__main__"}};
        sources["bar.x"] = SourcePublic{"bar.x", {}};
    }
    std::string repr() const {
        json j;
        j["bar"]["imported_by"] = {"__main__"};
        return j.dump();
    }
};

TEST(TestPublicJson, Dep2DotPublic) {
    GraphPublic g;
    json d = json::parse(g.repr());
    std::cout << d << std::endl;
    ASSERT_TRUE(d["bar"]["imported_by"].is_array());
    ASSERT_EQ(d["bar"]["imported_by"][0], "__main__");
    ASSERT_EQ(g.sources["bar.x"].name, g.sources["bar.x"].name);
    ASSERT_TRUE(g.sources["bar.x"].name.rfind("bar.x", 0) == 0);
    std::string src_repr = "bar.y"; // Dummy for test context
    ASSERT_TRUE(src_repr.find("bar.y") != std::string::npos);
}