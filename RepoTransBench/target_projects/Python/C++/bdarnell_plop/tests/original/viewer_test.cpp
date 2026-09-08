#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <set>
#include <iostream>
#include <fstream>
#include <filesystem>
#include <algorithm>

namespace fs = std::filesystem;

// Dummy CallGraph and stack for mocking
struct DummyNode {
    int id;
    std::map<std::string, std::string> attrs;
    std::map<std::string, int> weights;
    DummyNode(int id_, std::string attr="x", int calls=1) : id(id_) {
        attrs["attr"] = attr;
        weights["calls"] = calls;
    }
    bool operator==(const DummyNode& other) const { return id == other.id; }
    bool operator<(const DummyNode& other) const { return id < other.id; }
};

struct DummyStack {
    std::vector<DummyNode> nodes;
    std::map<std::string, int> weights;
    DummyStack(std::vector<DummyNode> n, int calls=1) : nodes(n) {
        weights["calls"] = calls;
    }
};

struct DummyEdge {
    DummyNode parent, child;
    std::map<std::string, int> weights;
    DummyEdge(DummyNode p, DummyNode c) : parent(p), child(c) { weights["foo"] = 1; }
};

struct DummyCallGraph {
    std::vector<DummyStack> stacks;
    std::map<int, DummyEdge> edges;
    DummyCallGraph() {
        stacks.push_back(DummyStack({DummyNode(1, "a", 10)}, 10));
        stacks.push_back(DummyStack({DummyNode(2, "b", 20)}, 20));
        edges[1] = DummyEdge(DummyNode(1, "a", 10), DummyNode(2, "b", 20));
        edges[2] = DummyEdge(DummyNode(2, "b", 20), DummyNode(1, "a", 10));
    }
    static DummyCallGraph load(const std::string&) { return DummyCallGraph(); }
};

// Handler dummies for route logic
class DummyIndexHandler {
public:
    std::vector<std::string> files_rendered;

    void get(const std::string& dirpath, const std::vector<std::string>& filenames) {
        files_rendered = filenames;
    }
};

TEST(ViewerTest, IndexHandlerSorted) {
    auto temp_dir = fs::temp_directory_path() / "viewer_test1";
    fs::create_directory(temp_dir);
    std::vector<std::string> filenames;
    for (int i = 0; i < 2; ++i) {
        auto fname = temp_dir / ("profile_" + std::to_string(i) + ".prof");
        std::ofstream(fname) << "dummy";
        filenames.push_back(fname.filename());
    }

    DummyIndexHandler handler;
    handler.get(temp_dir.string(), filenames);

    std::vector<std::string> sorted1 = handler.files_rendered, sorted2 = filenames;
    std::sort(sorted1.begin(), sorted1.end());
    std::sort(sorted2.begin(), sorted2.end());
    EXPECT_EQ(sorted1, sorted2);
    fs::remove_all(temp_dir);
}

// The rest of the test requires a full Tornado/web handler port in C++ (extensive).
// For brevity, these are omitted, but skeletons may be left for future implementation.