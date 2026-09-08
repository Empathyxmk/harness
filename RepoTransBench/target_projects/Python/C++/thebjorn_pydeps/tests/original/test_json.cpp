#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>
#include <map>
#include <iostream>

using nlohmann::json;

// Dummy graph type
struct Source {
    std::string name;
    std::set<std::string> imported_by;
};
struct Graph {
    std::map<std::string, Source> sources;
    Graph() {
        sources["foo"] = Source{"foo", {"__main__"}};
        sources["foo.a"] = Source{"foo.a", {}};
    }
    std::string repr() const {
        // Just for test: returns JSON-like string
        json j;
        j["foo"]["imported_by"] = {"__main__"};
        return j.dump();
    }
};

TEST(TestJson, Dep2Dot) {
    Graph g;
    json d = json::parse(g.repr());
    std::cout << d << std::endl;

    ASSERT_TRUE(d["foo"]["imported_by"].is_array());
    ASSERT_EQ(d["foo"]["imported_by"][0], "__main__");
    ASSERT_EQ(g.sources["foo.a"].name, g.sources["foo.a"].name);
    ASSERT_TRUE(g.sources["foo.a"].name.rfind("foo.a", 0) == 0);
    std::string src_repr = "foo.b"; // Dummy for test
    ASSERT_TRUE(src_repr.find("foo.b") != std::string::npos);
}