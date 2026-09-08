#include <gtest/gtest.h>
#include <set>
#include <string>
#include <iostream>

// Dummy implementations for simulation
std::set<std::string> simpledeps_skip(const std::string& fname, const std::string& args = "") {
    // Simulate based on args
    if (args.find("-x relimp.*") != std::string::npos) return {};
    if (args.find("-xx relimp.c") != std::string::npos && fname == "relimp")
        return {"relimp.b -> relimp.a", "relimp.c.d -> relimp.b"};
    if (args.find("--show-raw-deps") != std::string::npos && args.find("-x relimp.c") != std::string::npos)
        return {"relimp.b -> relimp.a"};
    if (args.find("-x relimp.c") != std::string::npos) return {"relimp.b -> relimp.a"};
    if (fname == "relimp")
        return {
            "relimp.b -> relimp.a",
            "relimp.c -> relimp.b"
        };
    return {};
}

TEST(TestSkip, NoSkip) {
    auto deps = simpledeps_skip("relimp");
    std::cout << "plain " << deps.size() << std::endl;
    ASSERT_EQ(deps, std::set<std::string>({
        "relimp.b -> relimp.a", "relimp.c -> relimp.b"
    }));
}

TEST(TestSkip, SkipModulePattern) {
    auto deps = simpledeps_skip("relimp", "-x relimp.*");
    std::cout << "-x " << deps.size() << std::endl;
    ASSERT_EQ(deps, std::set<std::string>());
}

TEST(TestSkip, SkipExactPattern) {
    auto deps = simpledeps_skip("relimp");
    ASSERT_EQ(deps, std::set<std::string>({
        "relimp.b -> relimp.a",
        "relimp.c.d -> relimp.b",
        "relimp.c -> relimp.b",
        "relimp.c -> relimp.a",
    }));

    auto deps2 = simpledeps_skip("relimp", "-xx relimp.c");
    ASSERT_EQ(deps2, std::set<std::string>({
        "relimp.b -> relimp.a",
        "relimp.c.d -> relimp.b",
    }));
}

TEST(TestSkip, SkipExact) {
    auto deps = simpledeps_skip("relimp", "-xx relimp.c");
    ASSERT_EQ(deps, std::set<std::string>{
        "relimp.b -> relimp.a"
    });
}

TEST(TestSkip, SkipModules) {
    auto deps = simpledeps_skip("relimp", "-x relimp.c");
    ASSERT_EQ(deps, std::set<std::string>{
        "relimp.b -> relimp.a"
    });
}

TEST(TestSkip, RawDeps) {
    auto deps = simpledeps_skip("relimp", "--show-raw-deps -x relimp.c");
    ASSERT_EQ(deps, std::set<std::string>{"relimp.b -> relimp.a"});
}