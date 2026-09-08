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

TEST(PublicConfigAdditional, LoadYamlAndPy) {
    // YAML file test with different content
    std::string yaml = "K: 789\nL:\n  M: false\n";
    std::string yamlPath = "public_test_config_additional_yaml.yaml";
    TmpFileHelper tmpYaml(yamlPath, yaml);
    CfgNode cfg(true);
    cfg.mergeFromFile(tmpYaml.path());
    EXPECT_EQ(cfg.get<int>("K"), 789);
    auto L = cfg.getNode("L");
    EXPECT_FALSE(L->get<bool>("M"));

    // Python file test - in C++, this throws (not supported)
    std::string pyPath = "public_test_config_additional_py.py";
    std::string pyContent = "cfg = dict(Z=[7,8,9], Y=dict(X='baz'))";
    TmpFileHelper tmpPy(pyPath, pyContent);
    CfgNode cfg2(true);
    EXPECT_THROW(cfg2.mergeFromFile(tmpPy.path()), std::runtime_error);
}

TEST(PublicConfigAdditional, LoadCfgFileObjectYaml) {
    // C++: parse YAML and merge dict
    std::string yaml = "A: 88\nB: [4, 5, 6]";
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
    EXPECT_EQ(cfg.get<int>("A"), 88);
    EXPECT_EQ(cfg.get<std::vector<int>>("B"), std::vector<int>({4,5,6}));
}

TEST(PublicConfigAdditional, LoadCfgFileObjectPy) {
    // Simulate
    CfgNode cfg({}, true);
    cfg.set("ALPHA", std::vector<int>({100,200,300}));
    EXPECT_EQ(cfg.get<std::vector<int>>("ALPHA"), std::vector<int>({100,200,300}));
}

TEST(PublicConfigAdditional, DumpAndLoadRoundtrip) {
    CfgNode cfg;
    cfg.set("foo", 21);
    cfg.set("bar", std::string("hello world"));
    std::string dumped = cfg.dump();

    std::string fn = "public_config_additional_dumped.yaml";
    {
        std::ofstream ofs(fn);
        ofs << dumped;
    }
    CfgNode new_cfg(true);
    new_cfg.mergeFromFile(fn);
    std::remove(fn.c_str());
    EXPECT_EQ(new_cfg.get<int>("foo"), 21);
    EXPECT_EQ(new_cfg.get<std::string>("bar"), "hello world");
}

TEST(PublicConfigAdditional, WrongExtension) {
    std::string fn = "public_config_additional_bad.txt";
    {
        std::ofstream ofs(fn); ofs << "BAR=3";
    }
    EXPECT_THROW({
        CfgNode::loadCfg(fn);
    }, std::exception);
    std::remove(fn.c_str());
}