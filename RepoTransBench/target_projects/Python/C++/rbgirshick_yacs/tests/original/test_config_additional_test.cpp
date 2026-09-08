#include <gtest/gtest.h>
#include <fstream>
#include <cstdio>
#include "yacs/cfg_node.h"

class TmpFileHelper {
    std::string path_;
public:
    TmpFileHelper(const std::string& path, const std::string& contents)
        : path_(path) {
        std::ofstream ofs(path_);
        ofs << contents;
    }
    ~TmpFileHelper() { std::remove(path_.c_str()); }
    std::string path() const { return path_; }
};

TEST(ConfigAdditional, LoadYamlAndPy) {
    // YAML file test
    std::string yaml = "A: 123\nB:\n  C: true\n";
    std::string yamlPath = "test_config_additional_test_yaml.yaml";
    TmpFileHelper tmpYaml(yamlPath, yaml);
    CfgNode cfg(true);
    cfg.mergeFromFile(tmpYaml.path());
    EXPECT_EQ(cfg.get<int>("A"), 123);
    auto B = cfg.getNode("B");
    EXPECT_TRUE(B->get<bool>("C"));

    // Python file test - in C++, this throws (not supported)
    std::string pyPath = "test_config_additional_test_py.py";
    std::string pyContent = "cfg = dict(D=456, E=dict(F='bar'))";
    TmpFileHelper tmpPy(pyPath, pyContent);
    CfgNode cfg2(true);
    EXPECT_THROW(cfg2.mergeFromFile(tmpPy.path()), std::runtime_error);
}

TEST(ConfigAdditional, LoadCfgFileObjectYaml) {
    // C++: Just call mergeFromDict after parsing YAML
    std::string yaml = "X: 1\nY: [1,2,3]";
    YAML::Node root = YAML::Load(yaml);
    std::unordered_map<std::string, CfgValue> dct;
    for(auto it = root.begin(); it != root.end(); ++it) {
        if(it->second.IsScalar()) {
            dct[it->first.as<std::string>()] = it->second.as<int>();
        } else if(it->second.IsSequence()) {
            std::vector<int> vec;
            for(const auto& v : it->second) vec.push_back(v.as<int>());
            dct[it->first.as<std::string>()] = vec;
        }
    }
    CfgNode cfg(true);
    cfg.mergeFromDict(dct);
    EXPECT_EQ(cfg.get<int>("X"), 1);
    EXPECT_EQ(cfg.get<std::vector<int>>("Y"), std::vector<int>({1,2,3}));
}

TEST(ConfigAdditional, LoadCfgFileObjectPy) {
    // Simulating Python local-gather for top-level variables.
    // In C++, this would just read a C++ map
    // For demo, simulate reading a {"A": [1,2,3]}
    CfgNode cfg({}, true);
    cfg.set("A", std::vector<int>({1,2,3}));
    EXPECT_EQ(cfg.get<std::vector<int>>("A"), std::vector<int>({1,2,3}));
}

TEST(ConfigAdditional, DumpAndLoadRoundtrip) {
    CfgNode cfg;
    cfg.set("foo", 3);
    cfg.set("bar", 6);
    std::string dumped = cfg.dump();

    std::string tmpfn = "test_config_dumped.yaml";
    {
        std::ofstream ofs(tmpfn);
        ofs << dumped;
    }
    CfgNode new_cfg(true);
    new_cfg.mergeFromFile(tmpfn);
    std::remove(tmpfn.c_str());
    EXPECT_EQ(new_cfg.get<int>("foo"), 3);
    EXPECT_EQ(new_cfg.get<int>("bar"), 6);
}

TEST(ConfigAdditional, WrongExtension) {
    std::string fn = "test_config_additional_bad.txt";
    {
        std::ofstream ofs(fn); ofs << "FOO=2";
    }
    EXPECT_THROW({
        CfgNode::loadCfg(fn);
    }, std::exception);
    std::remove(fn.c_str());
}