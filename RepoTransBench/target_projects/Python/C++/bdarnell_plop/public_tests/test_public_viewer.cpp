#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <filesystem>
#include <fstream>
#include <algorithm>

namespace fs = std::filesystem;

struct DummyNodeP {
    int id;
    std::map<std::string, std::string> attrs;
    std::map<std::string, int> weights;
    DummyNodeP(int id_, std::string attr="y", int calls=2) : id(id_) {
        attrs["attr"] = attr;
        weights["calls"] = calls;
    }
    bool operator==(const DummyNodeP& other) const { return id == other.id; }
    bool operator<(const DummyNodeP& other) const { return id < other.id; }
};

struct DummyStackP {
    std::vector<DummyNodeP> nodes;
    std::map<std::string, int> weights;
    DummyStackP(std::vector<DummyNodeP> n, int calls=2) : nodes(n) {
        weights["calls"] = calls;
    }
};

struct DummyEdgeP {
    DummyNodeP parent, child;
    std::map<std::string, int> weights;
    DummyEdgeP(DummyNodeP p, DummyNodeP c) : parent(p), child(c) { weights["bar"] = 3; }
};

struct DummyCallGraphP {
    std::vector<DummyStackP> stacks;
    std::map<int, DummyEdgeP> edges;
    DummyCallGraphP() {
        stacks.push_back(DummyStackP({DummyNodeP(11, "aa", 13)}, 13));
        stacks.push_back(DummyStackP({DummyNodeP(22, "bb", 17)}, 17));
        edges[1] = DummyEdgeP(DummyNodeP(11, "aa", 13), DummyNodeP(22, "bb", 17));
        edges[2] = DummyEdgeP(DummyNodeP(22, "bb", 17), DummyNodeP(11, "aa", 13));
    }
    static DummyCallGraphP load(const std::string&) { return DummyCallGraphP(); }
};

// Handler dummies for testing
class DummyIndexHandlerP {
public:
    std::vector<std::string> files_rendered;
    void get(const std::string& dirpath, const std::vector<std::string>& filenames) {
        files_rendered = filenames;
    }
};

TEST(PublicViewerTest, IndexHandlerSorted) {
    auto temp_dir = fs::temp_directory_path() / "public_viewer_test1";
    fs::create_directory(temp_dir);
    std::vector<std::string> filenames;
    for (int i = 0; i < 3; ++i) {
        auto fname = temp_dir / ("sample_" + std::to_string(i) + ".prof");
        std::ofstream(fname) << "data";
        filenames.push_back(fname.filename());
    }

    DummyIndexHandlerP handler;
    handler.get(temp_dir.string(), filenames);
    std::vector<std::string> sorted1 = handler.files_rendered, sorted2 = filenames;
    std::sort(sorted1.begin(), sorted1.end());
    std::sort(sorted2.begin(), sorted2.end());
    EXPECT_EQ(sorted1, sorted2);
    fs::remove_all(temp_dir);
}

// Other HTTP/view tests require real server routing - skip or simulate.