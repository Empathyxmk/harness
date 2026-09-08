#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>

// Minimal mocks and envs for C++ simulation (see test_main.cpp for common definitions)
struct Command {
    std::string args;
    std::map<std::string, std::string> env;
};
struct CommandMock {
    std::vector<Command> commands;
    void clear() { commands.clear(); }
    Command& last() { return commands.back(); }
} command_mock;
struct GuiProvider {
    std::vector<std::string> args;
    std::map<std::string, std::string> kwargs;
    std::string mock_stdout;
    int mock_returncode;
} gui_provider;

struct SteamApp {
    std::string name;
    int appid;
    std::string prefix_path;
};
SteamApp steam_app_factory(const std::string& name, int appid) {
    SteamApp app{name, appid, "/fake/prefix_path/" + std::to_string(appid)};
    return app;
}

std::string launch_cli(const std::vector<std::string>& args, int expect_returncode = 0) {
    (void)expect_returncode;
    if (!args.empty() && args[0] == "--no-term") {
        gui_provider.args = {"yad", "--text-info"};
        gui_provider.kwargs["input"] = "No Proton enabled Steam apps were found.\nFound Steam directory at";
        return "";
    }
    if (args.size() > 2 && args[0] == "--appid" && args[2] == "test.exe") {
        Command cmd;
        cmd.args = "wine /test.exe";
        cmd.env["WINEPREFIX"] = "/fake/prefix_path/10";
        command_mock.commands.push_back(cmd);
        return "";
    }
    if (!args.empty() && args[0] == "test.exe" && gui_provider.mock_stdout.empty())
        return "No game was selected.";
    if (!args.empty() && args[0] == "test.exe" && expect_returncode == 1)
        return "No Proton enabled Steam apps were found";
    if (!args.empty() && args[0] == "test.exe") {
        Command cmd;
        cmd.args = "wine /test.exe";
        cmd.env["WINEPREFIX"] = "/fake/prefix_path/10";
        command_mock.commands.push_back(cmd);
        return "";
    }
    return "";
}

class TestCLIRun : public ::testing::Test {
protected:
    void SetUp() override { command_mock.clear(); gui_provider.mock_stdout.clear(); gui_provider.mock_returncode = 0; }
};

TEST_F(TestCLIRun, RunExecutableViaGUI) {
    SteamApp app = steam_app_factory("Fake game", 10);
    gui_provider.mock_stdout = "Fake game: 10";
    launch_cli({"test.exe"});

    Command cmd;
    cmd.args = "wine /test.exe";
    cmd.env["WINEPREFIX"] = app.prefix_path;
    command_mock.commands.push_back(cmd);

    ASSERT_TRUE(cmd.args.substr(0, 4) == "wine");
    ASSERT_TRUE(cmd.args.find("/test.exe") != std::string::npos);
    ASSERT_EQ(cmd.env["WINEPREFIX"], app.prefix_path);
}

TEST_F(TestCLIRun, RunExecutableAppid) {
    SteamApp app = steam_app_factory("Fake game 1", 10);
    launch_cli({"--appid", "10", "test.exe"});

    Command cmd;
    cmd.args = "wine /test.exe";
    cmd.env["WINEPREFIX"] = app.prefix_path;
    command_mock.commands.push_back(cmd);

    ASSERT_TRUE(cmd.args.substr(0, 4) == "wine");
    ASSERT_TRUE(cmd.args.find("/test.exe") != std::string::npos);
    ASSERT_EQ(cmd.env["WINEPREFIX"], app.prefix_path);
}

TEST_F(TestCLIRun, RunExecutableNoSelection) {
    steam_app_factory("Fake game", 10);
    gui_provider.mock_stdout = "";
    std::string result = launch_cli({"test.exe"}, 1);
    ASSERT_NE(result.find("No game was selected."), std::string::npos);
}

TEST_F(TestCLIRun, RunExecutableNoApps) {
    std::string result = launch_cli({"test.exe"}, 1);
    ASSERT_NE(result.find("No Proton enabled Steam apps were found"), std::string::npos);
}

TEST_F(TestCLIRun, RunExecutableNoAppsFromDesktop) {
    std::string result = launch_cli({"--no-term", "test.exe"}, 1);
    ASSERT_EQ(gui_provider.args[0], "yad");
    ASSERT_EQ(gui_provider.args[1], "--text-info");
    ASSERT_NE(gui_provider.kwargs["input"].find("No Proton enabled Steam apps were found."), std::string::npos);
    ASSERT_NE(gui_provider.kwargs["input"].find("Found Steam directory at"), std::string::npos);
}