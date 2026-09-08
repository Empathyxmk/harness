#include "gtest/gtest.h"
#include <string>
#include <vector>
#include <algorithm>

/*
Original test_noxfile.py tests the logic of building/testing/lint "session" API and monkeypatching.

In C++ we do not have Python's noxfile.py or session concept.
We simulate the test intent: verify "lint" installs/runs flake8, "build_and_check_dists" calls install/run, etc.

We'll provide minimal stubs and simulate the "session" API.
*/

struct DummySession {
    std::vector<std::vector<std::string>> installed;
    std::vector<std::vector<std::string>> runs;
    std::vector<std::string> run_names;
    std::vector<std::string> posargs;
    void install(const std::initializer_list<const char*>& args) {
        std::vector<std::string> t;
        for (const char* s : args) t.emplace_back(s);
        installed.push_back(t);
    }
    void run(const std::initializer_list<const char*>& args) {
        std::vector<std::string> t;
        for (const char* s : args) t.emplace_back(s);
        runs.push_back(t);
        if (!t.empty()) run_names.push_back(t[0]);
    }
};

void lint(DummySession& s) {
    s.install({"flake8"});
    s.run({"flake8", "--version"});
}

void build_and_check_dists(DummySession& s) {
    s.install({"build"});
    s.install({"twine"});
    s.run({"python", "-m", "build"});
    s.run({"twine", "check"});
}

void tests(DummySession& s, bool buildRan = false) {
    if (!buildRan) build_and_check_dists(s);
    s.run({"pytest"});
}

TEST(NoxfileTests, LintRunsAndInstalls) {
    DummySession s;
    lint(s);
    bool found_flake8_install = false;
    for (const auto& arr : s.installed)
        found_flake8_install = found_flake8_install || (std::find(arr.begin(), arr.end(), "flake8") != arr.end());
    EXPECT_TRUE(found_flake8_install);

    bool found_flake8_run = false;
    for (const auto& arr : s.runs)
        found_flake8_run = found_flake8_run || (std::find(arr.begin(), arr.end(), "flake8") != arr.end());
    EXPECT_TRUE(found_flake8_run);
}

TEST(NoxfileTests, BuildAndCheckDistsInvocations) {
    DummySession s;
    build_and_check_dists(s);
    EXPECT_FALSE(s.installed.empty());
    EXPECT_FALSE(s.runs.empty());
}

TEST(NoxfileTests, TestsInvokesBuild) {
    DummySession s;
    tests(s);
    // Should have at least a python build and a pytest run
    bool found_pytest = false, found_build = false;
    for (const auto& arr : s.runs) {
        if (!arr.empty() && arr[0] == "pytest") found_pytest = true;
        if (!arr.empty() && arr[0] == "python") found_build = true;
    }
    EXPECT_TRUE(found_pytest);
    EXPECT_TRUE(found_build);
}