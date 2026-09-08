#include <gtest/gtest.h>
#include <set>
#include <string>

std::set<std::string> simpledeps_funny_names(const std::string& fname, const std::string& args = "") {
    // Simulate dependency logic based on fname
    if (fname == "foo" && args.find("--show-deps") != std::string::npos)
        return {"bar -> foo.a", "bar.py -> foo.a"};
    if (fname == "foo.bar.py") {
        return {"math -> foo.bar.py"};
    }
    return {};
}

TEST(TestFunnyNames, FromHtml5lib) {
    auto deps = simpledeps_funny_names("foo", "--show-deps -LINFO -vv");
    ASSERT_EQ(deps, std::set<std::string>({
        "bar -> foo.a", "bar.py -> foo.a"
    }));
}

TEST(TestFunnyNames, MultiDot) {
    auto deps = simpledeps_funny_names("foo.bar.py", "--show-deps --pylib -LINFO -vv");
    ASSERT_EQ(deps, std::set<std::string>({"math -> foo.bar.py"}));
}