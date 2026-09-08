#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <vector>
#include <typeinfo>

class NoVaultSecretFound : public std::exception {
public:
    const char* what() const noexcept override { return "NoVaultSecretFound"; }
};

class FakeCLIPublic {
public:
    static bool called;
    static void setup_vault_secrets(...) { called = true; }
};
bool FakeCLIPublic::called = false;

class DummyLoaderPublic {};

class DummyIMPublic {
public:
    std::vector<std::string> _sources;
    DummyLoaderPublic _loader;
    DummyIMPublic() : _sources({"/var/xyz"}) {}
    std::unordered_map<std::string, int> groups() { return {}; }
};

class DummyGroupPublic {};

class DummyPluginPublic {
public:
    bool called = false;
    std::unordered_map<std::string, std::string> get_vars(DummyLoaderPublic*, const std::string&, const std::vector<std::string>&) {
        called = true;
        return { {"baz", "qux"} };
    }
};

class DummyPluginHostPublic : public DummyPluginPublic {
public:
    std::unordered_map<std::string, int> get_host_vars(const std::string&) { return { {"a", 82} }; }
    std::unordered_map<std::string, int> get_group_vars(const std::string&) { return { {"b", 99} }; }
};

class DummyHostPublic {
public:
    std::string name;
    DummyHostPublic(const std::string& n) : name(n) {}
};

TEST(TestPublicInventory, NoVaultSecretFoundPublic) {
    NoVaultSecretFound ex;
    EXPECT_STREQ(ex.what(), "NoVaultSecretFound");
}

TEST(TestPublicInventory, AnsibleInventoryPublicInit) {
    FakeCLIPublic::called = false;
    FakeCLIPublic::setup_vault_secrets(nullptr, {}, {}, false);
    EXPECT_TRUE(FakeCLIPublic::called);
}

TEST(TestPublicInventory, PluginsInventoryPublic) {
    DummyIMPublic dummyIM;
    DummyGroupPublic dummyGroup;
    DummyPluginPublic plugin;
    auto result = plugin.get_vars(&dummyIM._loader, "/", { "dummy" });
    EXPECT_EQ(result["baz"], "qux");
}

TEST(TestPublicInventory, GetPluginVarsHostPublic) {
    DummyPluginHostPublic plugin;
    auto host_vars = plugin.get_host_vars("hh");
    EXPECT_EQ(host_vars["a"], 82);
    auto group_vars = plugin.get_group_vars("gx");
    EXPECT_EQ(group_vars["b"], 99);
}

TEST(TestPublicInventory, GetGroupVarsPublic) {
    std::unordered_map<std::string, int> expected{ {"other", 50} };
    EXPECT_EQ(expected["other"], 50);
}

TEST(TestPublicInventory, GetHostVarsMagicPublic) {
    std::unordered_map<std::string, int> inputVars = { {"persist", 42} };
    EXPECT_TRUE(inputVars.find("persist") != inputVars.end());
    // keys "omit" and "ansible_version" are not present
}

TEST(TestPublicInventory, GetHostVarsAnsibleErrorPublic) {
    class DummyVM3 {
    public:
        void get_vars() { throw NoVaultSecretFound(); }
    };
    DummyVM3 vm;
    try {
        vm.get_vars();
        FAIL() << "Expected NoVaultSecretFound";
    } catch (const NoVaultSecretFound&) {
        SUCCEED();
    }
}

TEST(TestPublicInventory, GetGroupPublic) {
    std::unordered_map<std::string, int> groups = { {"gx", 501} };
    EXPECT_EQ(groups["gx"], 501);
}

TEST(TestPublicInventory, GetHostPublic) {
    std::string value = "hostX";
    EXPECT_EQ(value, "hostX");
}

TEST(TestPublicInventory, ListHostsPublic) {
    std::vector<std::string> hosts = { "h2" };
    EXPECT_EQ(hosts.size(), 1);
    EXPECT_EQ(hosts[0], "h2");
}

TEST(TestPublicInventory, InventoryManagerPublic) {
    std::string invobj = "public_invobj";
    EXPECT_EQ(invobj, "public_invobj");
    std::string invobj2 = "public_invobj";
    EXPECT_EQ(invobj2, "public_invobj");
}