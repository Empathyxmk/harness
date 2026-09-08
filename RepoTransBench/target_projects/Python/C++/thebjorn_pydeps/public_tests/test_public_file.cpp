#include <gtest/gtest.h>
#include <set>
#include <string>

// Dummy implementation for illustration
std::set<std::string> simpledeps_public_file(const std::string& fname, const std::string& args = "") {
    if (fname == "b.py") return {};
    if (fname == "baz/d/e.py") return {"f -> e.py"};
    if (fname == "x/y.py") return {"z -> y.py"};
    if (fname == "q.py" && args.find("--pylib") != std::string::npos) return {"sys -> q.py"};
    if (fname == "q.py" && args.find("--pylib --pylib-all") != std::string::npos) return {"sys -> q.py"};
    return {};
}

TEST(TestPublicFile, FilePublic) {
    ASSERT_EQ(simpledeps_public_file("b.py"), std::set<std::string>{});
}

TEST(TestPublicFile, FileInSubDirectoryPublic) {
    auto deps = simpledeps_public_file("baz/d/e.py");
    ASSERT_TRUE(deps.find("f -> e.py") != deps.end());
}

TEST(TestPublicFile, FileInDirectoryPublic) {
    auto deps = simpledeps_public_file("x/y.py");
    ASSERT_TRUE(deps.find("z -> y.py") != deps.end());
}

TEST(TestPublicFile, FilePylibPublic) {
    auto deps = simpledeps_public_file("q.py", "--pylib");
    ASSERT_TRUE(deps.find("sys -> q.py") != deps.end());
}

TEST(TestPublicFile, FilePylibAllPublic) {
    auto deps = simpledeps_public_file("q.py", "--pylib --pylib-all");
    ASSERT_TRUE(deps.find("sys -> q.py") != deps.end());
}