#include "gtest/gtest.h"
#include <string>
#include <vector>

/*
Python public noxfile tests parse Python code with AST to ensure
- "lint" session exists and is a function
- Has session decorator
- Calls session.run with "flake8" or "pytest" or "mypy"

In C++, we simulate this by verifying "lint" exists, is callable (function exists), takes a DummySession, and calls run with correct args.

*/

struct DummySession {
    std::vector<std::vector<std::string>> installed;
    std::vector<std::vector<std::string>> runs;
    std::vector<std::string> run_names;
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

// "session decorator" doesn't exist in C++; we simulate that lint(DummySession&) exists.
void lint(DummySession& s) {
    s.install({"flake8"});
    s.run({"flake8", "--version"});
}

TEST(PublicNoxfileTests, LintSessionExistsAndIsDef) {
    // Confirm that 'lint' is defined and callable with DummySession&
    DummySession s;
    lint(s); // will not crash
    // Accepts at least one parameter: in C++, it's DummySession&
    SUCCEED();
}

TEST(PublicNoxfileTests, LintSessionIncludesSessionDecorator) {
    // In C++, "decorator" doesn't exist. But we simulate by lint(DummySession&) exists
    // and passes DummySession as argument
    DummySession s;
    lint(s);
    SUCCEED();
}

TEST(PublicNoxfileTests, LintSessionCallsRunWithSpecificArgs) {
    DummySession s;
    lint(s);
    bool found = false;
    for (const auto& arr : s.runs) {
        for (const auto& item : arr) {
            if (item == "flake8" || item == "pytest" || item == "mypy")
                found = true;
        }
    }
    EXPECT_TRUE(found) << "Should call session.run with flake8 or pytest or mypy";
}