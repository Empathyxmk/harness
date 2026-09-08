#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <regex>
#include "dummy_logic.h"

class TestRunResult {
public:
    int rc;
    TestRunResult(int rc_) : rc(rc_) {}
};
class TestDummyFile {
public:
    std::string content_string;
    explicit TestDummyFile(const std::string& content) : content_string(content) {}
    bool contains(const std::string& needle) const { return content_string.find(needle) != std::string::npos; }
};
class TestDummyUser {
public:
    std::vector<std::string> groups;
    explicit TestDummyUser(const std::vector<std::string>& groups_) : groups(groups_) {}
};
class TestDummyHost {
public:
    std::string docker_version;
    std::string docker_compose_version;
    std::string daemon_json_content;
    std::string environment_file;
    std::string options_file;
    std::string custom_conf_file;
    std::string cron_file;
    std::vector<std::string> user_groups;

    TestDummyHost() {
        docker_version = "Docker version 20.10.10, build b485636";
        docker_compose_version = "Docker Compose version v2.3.3";
        daemon_json_content = "{\"log-driver\":\"journald\",\"dns\":[\"8.8.8.8\"]}";
        environment_file = "Environment=\"HTTP_PROXY=http://proxy\"\nEnvironment=\"HTTPS_PROXY=https://proxy\"";
        options_file = "-H fd:// --debug";
        custom_conf_file = "ATest";
        cron_file = "0 * * * * test docker system prune -af";
        user_groups = {"docker", "test"};
    }
    TestRunResult run(const std::string& cmd) {
        if (cmd.find("docker --version") != std::string::npos) return TestRunResult(0);
        if (cmd.find("docker compose version") != std::string::npos) return TestRunResult(0);
        if (cmd.find("python3-docker") != std::string::npos) return TestRunResult(0);
        return TestRunResult(1);
    }
    std::string check_output(const std::string& cmd) {
        if (cmd == "docker --version") return docker_version;
        if (cmd == "docker compose version") return docker_compose_version;
        return "UNKNOWN";
    }
    TestDummyUser user(const std::string&) { return TestDummyUser(user_groups); }
    TestDummyFile file(const std::string& path) {
        if (path == "/etc/docker/daemon.json") return TestDummyFile(daemon_json_content);
        if (path == "/etc/systemd/system/docker.service.d/environment.conf") return TestDummyFile(environment_file);
        if (path == "/etc/systemd/system/docker.service.d/options.conf") return TestDummyFile(options_file);
        if (path == "/etc/systemd/system/docker.service.d/custom.conf") return TestDummyFile(custom_conf_file);
        if (path == "/etc/cron.d/docker-disk-clean-up") return TestDummyFile(cron_file);
        return TestDummyFile("");
    }
};

class HostMockFixture : public ::testing::Test {
protected:
    TestDummyHost host;
};

TEST_F(HostMockFixture, DockerVersion) {
    EXPECT_EQ(0, host.run("docker --version").rc);
}
TEST_F(HostMockFixture, PinnedDockerVersion) {
    std::string existing = host.check_output("docker --version");
    host.run("sudo apt-get update");
    host.run("sudo apt-get upgrade");
    std::string after = host.check_output("docker --version");
    EXPECT_EQ(existing, after);
}
TEST_F(HostMockFixture, DockerComposeV2Version) {
    EXPECT_EQ(0, host.run("docker compose version").rc);
}
TEST_F(HostMockFixture, PinnedDockerComposeV2Version) {
    std::string existing = host.check_output("docker compose version");
    host.run("sudo apt-get update");
    host.run("sudo apt-get upgrade");
    std::string after = host.check_output("docker compose version");
    EXPECT_EQ(existing, after);
}
TEST_F(HostMockFixture, AbleToAccessDockerWithoutRoot) {
    EXPECT_NE(std::find(host.user("test").groups.begin(), host.user("test").groups.end(), "docker"), host.user("test").groups.end());
}
TEST_F(HostMockFixture, DaemonJsonIsConfigured) {
    TestDummyFile daemon_json = host.file("/etc/docker/daemon.json");
    EXPECT_TRUE(daemon_json.contains("journald"));
    EXPECT_TRUE(daemon_json.contains("8.8.8.8"));
}
TEST_F(HostMockFixture, CustomizedEnvironmentSystemdUnitFile) {
    std::string file_contents = host.file("/etc/systemd/system/docker.service.d/environment.conf").content_string;
    EXPECT_TRUE(std::regex_search(file_contents, std::regex("Environment=\"HTTP_PROXY=.*\"")));
    EXPECT_TRUE(std::regex_search(file_contents, std::regex("Environment=\"HTTPS_PROXY=.*\"")));
}
TEST_F(HostMockFixture, CustomizedDaemonFlagsSystemdUnitFile) {
    std::string file_contents = host.file("/etc/systemd/system/docker.service.d/options.conf").content_string;
    EXPECT_NE(file_contents.find("-H fd://"), std::string::npos);
    EXPECT_NE(file_contents.find("--debug"), std::string::npos);
}
TEST_F(HostMockFixture, CustomizedSystemdOverride) {
    std::string file_contents = host.file("/etc/systemd/system/docker.service.d/custom.conf").content_string;
    EXPECT_NE(file_contents.find("ATest"), std::string::npos);
}
TEST_F(HostMockFixture, DockerCleanUpCronJob) {
    std::string cron_conf = host.file("/etc/cron.d/docker-disk-clean-up").content_string;
    EXPECT_NE(cron_conf.find("test docker system prune -af"), std::string::npos);
}
TEST_F(HostMockFixture, PythonDockerModule) {
    EXPECT_EQ(0, host.run("python3-docker -c 'import docker'").rc);
}
TEST_F(HostMockFixture, DaemonJsonMissingKeys) {
    TestDummyFile f = host.file("/wrong/path");
    EXPECT_FALSE(f.contains("journald"));
    EXPECT_FALSE(f.contains("8.8.8.8"));
}
TEST_F(HostMockFixture, CustomizedEnvironmentSystemdUnitFileMissingKeys) {
    std::string file_contents = host.file("/wrong/path").content_string;
    EXPECT_FALSE(std::regex_search(file_contents, std::regex("Environment=\"HTTP_PROXY=.*\"")));
    EXPECT_FALSE(std::regex_search(file_contents, std::regex("Environment=\"HTTPS_PROXY=.*\"")));
}
TEST_F(HostMockFixture, FileObjectEmpty) {
    EXPECT_EQ(host.file("/nonexistent/path").content_string, "");
}
TEST(HostMockFixtureNoDocker, UserWithoutDockerGroup) {
    class NoDockerUser : public TestDummyUser {
    public:
        NoDockerUser() : TestDummyUser(std::vector<std::string>{"test"}) {}
    };
    class NoDockerHost : public TestDummyHost {
    public:
        TestDummyUser user(const std::string&) { return NoDockerUser(); }
    };
    NoDockerHost h;
    EXPECT_EQ(std::find(h.user("test").groups.begin(), h.user("test").groups.end(), "docker"), h.user("test").groups.end());
}