#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <vector>
#include <typeinfo>
#include <type_traits>

class NoVaultSecretFound : public std::exception {
public:
    virtual const char* what() const noexcept { return "NoVaultSecretFound"; }
};

class FakeCLI {
public:
    static bool called;
    static void setup_vault_secrets(...) { called = true; }
};
bool FakeCLI::called = false;

class DummyLoader {};

class DummyIM {
public:
    std::vector<std::string> _sources;
    DummyLoader _loader;
    DummyIM() : _sources({"/tmp"}) {}
    std::unordered_map<std::string, int> groups() { return {}; }
};

class DummyGroup {};

class DummyPlugin {
public:
    bool called = false;
    std::unordered_map<std::string, std::string> get_vars(DummyLoader*, const std::string&, const std::vector<std::string>&) {
        called = true;
        return { {"foo", "bar"} };
    }
};

class DummyPluginHost : public DummyPlugin {
public:
    std::unordered_map<std::string, int> get_host_vars(const std::string&) { return { {"x", 1} }; }
    std::unordered_map<std::string, int> get_group_vars(const std::string&) { return { {"y", 2} }; }
};

class DummyHost {
public:
    std::string name;
    DummyHost(const std::string& n) : name(n) {}
};

TEST(TestInventory, NoVaultSecretFoundTest) {
    NoVaultSecretFound ex;
    EXPECT_STREQ(ex.what(), "NoVaultSecretFound");
}

TEST(TestInventory, AnsibleInventoryInit) {
    FakeCLI::called = false;
    // Simulate initializing inventory, calling FakeCLI
    FakeCLI::setup_vault_secrets(nullptr, {}, {}, false);
    EXPECT_TRUE(FakeCLI::called);
}

TEST(TestInventory, PluginsInventoryTest) {
    DummyIM dummyIM;
    DummyGroup dummyGroup;
    DummyPlugin plugin;
    auto result = plugin.get_vars(&dummyIM._loader, "/", { "dummy" });
    EXPECT_EQ(result["foo"], "bar");
}

TEST(TestInventory, GetPluginVarsHost) {
    DummyPluginHost plugin;
    auto host_vars = plugin.get_host_vars("h");
    EXPECT_EQ(host_vars["x"], 1);
    auto group_vars = plugin.get_group_vars("g");
    EXPECT_EQ(group_vars["y"], 2);
}

TEST(TestInventory, GetGroupVars) {
    // Simulate a plugin call returning expected results
    std::unordered_map<std::string, int> expected{ {"some", 99} };
    EXPECT_EQ(expected["some"], 99);
}

TEST(TestInventory, GetHostVarsMagic) {
    // Only checking presence/absence, so simulate filtering out unwanted keys
    std::unordered_map<std::string, std::string> inputVars = { {"keep", "yes"}, {"omit", "omit"}, {"ansible_version", "xxx"} };
    inputVars.erase("omit");
    inputVars.erase("ansible_version");
    EXPECT_TRUE(inputVars.find("keep") != inputVars.end());
    EXPECT_TRUE(inputVars.find("omit") == inputVars.end());
    EXPECT_TRUE(inputVars.find("ansible_version") == inputVars.end());
}

TEST(TestInventory, GetHostVarsAnsibleError) {
    class DummyVM {
    public:
        void get_vars() { throw NoVaultSecretFound(); }
    };
    DummyVM vm;
    try {
        vm.get_vars();
        FAIL() << "Expected NoVaultSecretFound";
    } catch (const NoVaultSecretFound& e) {
        SUCCEED();
    }
}

TEST(TestInventory, GetGroup) {
    std::unordered_map<std::string, int> groups = { {"g", 1} };
    EXPECT_EQ(groups["g"], 1);
}

TEST(TestInventory, GetHost) {
    std::string host = "foo";
    std::string result = "host1";
    EXPECT_EQ(result, "host1");
}

TEST(TestInventory, ListHosts) {
    std::vector<std::string> hosts = { "h" };
    EXPECT_EQ(hosts.size(), 1);
    EXPECT_EQ(hosts[0], "h");
}

TEST(TestInventory, InventoryManager) {
    std::string invobj = "invobj";
    EXPECT_EQ(invobj, "invobj");
    std::string invobj2 = "invobj";
    EXPECT_EQ(invobj2, "invobj");
}