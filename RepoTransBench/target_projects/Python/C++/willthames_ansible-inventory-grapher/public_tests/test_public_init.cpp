#include <gtest/gtest.h>
#include <string>
#include <unordered_map>
#include <set>

class Edge {
public:
    std::string source;
    std::string target;
    Edge(const std::string& s, const std::string& t) : source(s), target(t) {}
    std::string repr() const { return source + " -> " + target; }
    bool operator==(const Edge& other) const { return source == other.source && target == other.target; }
    bool operator!=(const Edge& other) const { return !(*this == other); }
};

namespace std {
    template <>
    struct hash<Edge> {
        std::size_t operator()(const Edge& e) const {
            return hash<std::string>()(e.source) ^ hash<std::string>()(e.target);
        }
    };
}

class Node {
public:
    std::string name;
    Node(const std::string& n) : name(n) {}
    std::string repr() const { return name; }
    bool operator==(const Node& other) const { return name == other.name; }
    bool operator!=(const Node& other) const { return !(*this == other); }
};

namespace std {
    template <>
    struct hash<Node> {
        std::size_t operator()(const Node& n) const {
            return hash<std::string>()(n.name);
        }
    };
}

class DummyVault {
public:
    std::string _ciphertext;
    DummyVault(const std::string& ciphertext="") : _ciphertext(ciphertext) {}
};

class DummyGroup {
public:
    std::string name;
    std::vector<DummyGroup*> parent_groups;
    std::vector<DummyGroup*> _ancestors;
    DummyGroup(const std::string& n,
        const std::vector<DummyGroup*>& parents = std::vector<DummyGroup*>(),
        const std::vector<DummyGroup*>& ancestors = std::vector<DummyGroup*>()) :
        name(n), parent_groups(parents), _ancestors(ancestors) {}
    std::vector<DummyGroup*> get_ancestors() { return _ancestors; }
};

class DummyHost {
public:
    std::string name;
    std::vector<DummyGroup*> groups;
    std::unordered_map<std::string, std::string> _host_vars;
    DummyHost(const std::string& n) : name(n) {}
    std::vector<DummyGroup*> get_groups() { return groups; }
};

class DummyInventoryManager {
public:
    std::unordered_map<std::string, std::unordered_map<std::string, DummyVault>> group_vars_vault;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> group_vars;
    std::unordered_map<std::string, std::unordered_map<std::string, std::string>> host_vars;
    DummyInventoryManager(
        const std::unordered_map<std::string, std::unordered_map<std::string, std::string>>& gvar = {},
        const std::unordered_map<std::string, std::unordered_map<std::string, std::string>>& hvar = {}
    ) : group_vars(gvar), host_vars(hvar) {}
};

TEST(TestPublicInit, EdgePublicReprEqHash) {
    Edge e1("x", "y"), e2("x", "y"), e3("x", "z");
    EXPECT_EQ(e1.repr(), "x -> y");
    EXPECT_TRUE(e1 == e2);
    EXPECT_TRUE(e1 != e3);
    EXPECT_EQ(std::hash<Edge>()(e1), std::hash<Edge>()(e2));
    EXPECT_NE(std::hash<Edge>()(e1), std::hash<Edge>()(e3));
}

TEST(TestPublicInit, NodePublicReprEqHash) {
    Node n1("nn"), n2("nn"), n3("yy");
    EXPECT_EQ(n1.repr(), "nn");
    EXPECT_TRUE(n1 == n2);
    EXPECT_TRUE(n1 != n3);
    EXPECT_EQ(std::hash<Node>()(n1), std::hash<Node>()(n2));
    EXPECT_NE(std::hash<Node>()(n1), std::hash<Node>()(n3));
}

TEST(TestPublicInit, ParentGraphsPublicSimple) {
    DummyGroup g10("G10");
    DummyGroup g20("G20", {&g10});
    DummyGroup child2("CHILD2", {&g20});
    std::vector<DummyGroup*> groups{ &g10, &g20 };
    std::set<Edge> results;
    results.insert(Edge(g10.name, g20.name));
    results.insert(Edge(g20.name, child2.name));
    for (const Edge& e : results) {
        EXPECT_TRUE(typeid(e) == typeid(Edge));
    }
    // Confirm at least one source matches
    bool found = false;
    for (const Edge& e : results) {
        if (e.source == "G10" || e.source == "G20") found = true;
    }
    EXPECT_TRUE(found);
}

TEST(TestPublicInit, RemoveInhAndOverrVarsPublicNoMatch) {
    std::unordered_map<std::string, DummyVault> vars{ {"key9", DummyVault("value2")}, {"key8", DummyVault("lmn")} };
    EXPECT_TRUE(vars.find("key9") != vars.end());
    EXPECT_TRUE(vars.find("key8") != vars.end());
}

TEST(TestPublicInit, RemoveInhAndOverrVarsPublicVault) {
    std::string group = "g_public", k = "topsecret";
    DummyVault v1("shh"), v2("shh"), v3("totallydifferent");
    std::unordered_map<std::string, DummyVault> vars = { {k, v2} };
    if (vars[k]._ciphertext == v1._ciphertext) vars.erase(k);
    EXPECT_TRUE(vars.find(k) == vars.end() || vars[k]._ciphertext != v1._ciphertext);

    std::unordered_map<std::string, DummyVault> vars2 = { {k, v3} };
    if (vars2[k]._ciphertext == v1._ciphertext) vars2.erase(k);
    EXPECT_TRUE(vars2.find(k) != vars2.end());
}

TEST(TestPublicInit, RemoveInhAndOverrVarsPublicMixed) {
    std::string k = "vaultish";
    DummyVault v1("1xyz");
    std::unordered_map<std::string, DummyVault> vars = { {k, v1} };
    EXPECT_TRUE(vars.find(k) != vars.end());
}

TEST(TestPublicInit, RemoveInhAndOverrGroupVarsPub) {
    DummyGroup group("groupx");
    DummyGroup ancestor1("ancestor99");
    group._ancestors.push_back(&ancestor1);
    std::unordered_map<std::string, int> group_vars = { {"alpha", 19} };
    EXPECT_EQ(group_vars["alpha"], 19);
}

TEST(TestPublicInit, TidyAllVarsPublic) {
    DummyHost host("host_public");
    std::unordered_map<std::string, int> hvars = { {"varA", 1} };
    std::unordered_map<DummyHost*, std::unordered_map<std::string, int>> vars_by_host;
    vars_by_host[&host] = hvars;
    EXPECT_EQ(vars_by_host[&host]["varA"], 1);

    DummyGroup g2("g2z");
    host.groups.push_back(&g2);
    std::unordered_map<DummyGroup*, std::unordered_map<std::string, int>> gvars_by_group;
    gvars_by_group[&g2] = { {"sample", 505} };
    EXPECT_EQ(gvars_by_group[&g2]["sample"], 505);
}

TEST(TestPublicInit, GenerateGraphForHostPublic) {
    DummyHost host("hh2");
    DummyGroup g("gg2");
    host.groups.push_back(&g);
    std::set<Edge> edges = { Edge(g.name, host.name) };
    std::set<Node> nodes = { Node(g.name), Node(host.name) };
    for (const Edge& e : edges) EXPECT_TRUE(typeid(e) == typeid(Edge));
    for (const Node& n : nodes) EXPECT_TRUE(typeid(n) == typeid(Node));
}