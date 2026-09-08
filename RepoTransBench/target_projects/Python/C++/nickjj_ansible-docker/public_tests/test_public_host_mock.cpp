#include <gtest/gtest.h>
#include "host_mock.h"

TEST(PublicHostMock, AlternateHostname) {
    HostMock h("custom-server", "ubuntu", "debian");
    EXPECT_EQ(h.hostname, "custom-server");
    EXPECT_EQ(h.vars["inventory_hostname"], "custom-server");
}

TEST(PublicHostMock, DifferentOsFamily) {
    HostMock h("web01", "fedora", "redhat");
    EXPECT_EQ(h.os, "fedora");
    EXPECT_EQ(h.family, "redhat");
    EXPECT_EQ(h.vars["ansible_os_family"], "redhat");
}

TEST(PublicHostMock, GroupsAndVarsPublic) {
    HostMock h("server", "ubuntu", "debian", {"docker", "backend"}, {{"extra", "123"}});
    EXPECT_EQ(h.groups, std::vector<std::string>({"docker", "backend"}));
    EXPECT_EQ(h.vars["extra"], "123");
    EXPECT_EQ(h.vars["docker_host"], "unix:///var/run/docker.sock");
}

TEST(PublicHostMock, GetitemPublic) {
    HostMock h("server", "ubuntu", "debian", {}, {{"x", "100"}});
    EXPECT_EQ(h["x"], "100");
}

TEST(PublicHostMock, VarsMergingPublic) {
    HostMock h("merge", "ubuntu", "debian", {}, {{"a", "90"}, {"docker_host", "/tmp"}});
    EXPECT_EQ(h.vars["a"], "90");
    EXPECT_EQ(h.vars["docker_host"], "/tmp");
    EXPECT_NE(h.vars.find("inventory_hostname"), h.vars.end());
}

TEST(PublicHostMock, EnvVarPublic) {
    HostMock h("server", "ubuntu", "debian", {}, {{"env", "prod"}});
    EXPECT_EQ(h.vars["env"], "prod");
}

TEST(PublicHostMock, ReprOutputPublic) {
    HostMock h("visual", "redhat", "rhel");
    std::string rep = h.repr();
    EXPECT_NE(rep.find("visual"), std::string::npos);
    EXPECT_NE(rep.find("redhat"), std::string::npos);
    EXPECT_NE(rep.find("rhel"), std::string::npos);
}