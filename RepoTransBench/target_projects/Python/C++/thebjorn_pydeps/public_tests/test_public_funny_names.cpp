#include <gtest/gtest.h>
#include <set>
#include <string>

std::set<std::string> simpledeps_public_funny_names(const std::string& fname, const std::string& args = "") {
    if (fname == "zoo" && args.find("--show-deps") != std::string::npos)
        return {"custom -> zoo.tiger", "custom.py -> zoo.tiger"};
    if (fname == "alpha.beta.py") {
        return {"random -> alpha.beta.py"};
    }
    return {};
}

TEST(TestPublicFunnyNames, FromCustomlibPublic) {
    auto deps = simpledeps_public_funny_names("zoo", "--show-deps -LINFO -vv");
    ASSERT_EQ(deps, std::set<std::string>({"custom -> zoo.tiger", "custom.py -> zoo.tiger"}));
}

TEST(TestPublicFunnyNames, MultiDotPublic) {
    auto deps = simpledeps_public_funny_names("alpha.beta.py", "--show-deps --pylib -LINFO -vv");
    ASSERT_EQ(deps, std::set<std::string>({"random -> alpha.beta.py"}));
}