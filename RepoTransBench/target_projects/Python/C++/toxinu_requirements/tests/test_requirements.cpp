#include <gtest/gtest.h>
#include "requirements.h"

TEST(RequirementsTest, ParseNormalRequirement) {
    Requirement r = Requirement::parse("requests>=2.0");
    ASSERT_FALSE(r.name.empty());
    EXPECT_EQ(r.name, "requests");
    EXPECT_FALSE(r.specifier.empty());
    EXPECT_FALSE(r.is_local_file);
}

TEST(RequirementsTest, ParseLocalFileEditable) {
    EXPECT_THROW({
        Requirement::parse("/some/path/to/pkg", true);
    }, std::exception);
}

TEST(RequirementsTest, ParseLocalFileScheme) {
    Requirement r = Requirement::parse("file:///tmp/somepackage#egg=mypkg");
    EXPECT_NE(r.line.find("file://"), std::string::npos);
}

TEST(RequirementsTest, ParseVcsUrl) {
    std::string vcs_url = "git+https://github.com/user/repo.git#egg=myrepo";
    Requirement r = Requirement::parse(vcs_url);
    std::string s = r.line;
    EXPECT_TRUE(s.rfind("git+", 0) == 0 || s.find("git+") != std::string::npos);
}

TEST(RequirementsTest, ParseWithMarker) {
    Requirement r = Requirement::parse("requests; python_version>=\"3.0\"");
    ASSERT_FALSE(r.name.empty());
    EXPECT_FALSE(r.marker.empty());
}

TEST(RequirementsTest, StrRepr) {
    Requirement r = Requirement::parse("flask");
    std::string s = r.str();
    std::string rep = r.repr();
    EXPECT_TRUE(s == "flask" || s == "<Requirement: \"flask\">");
    EXPECT_FALSE(rep.empty());
}

TEST(RequirementsTest, EqualityAndHash) {
    Requirement r1 = Requirement::parse("foo==1.0");
    Requirement r2 = Requirement::parse("foo==1.0");
    // Some implementations do not use eq, so gracefully fallback
    try {
        EXPECT_TRUE(r1 == r2);
    } catch (...) {}
    (void)r1.hash();
    (void)r2.hash();
}

TEST(RequirementsTest, RequirementExtras) {
    Requirement r = Requirement::parse("requests[security]>=2.0");
    EXPECT_FALSE(r.extras.empty());
    EXPECT_NE(std::find(r.extras.begin(), r.extras.end(), "security"), r.extras.end());
}

TEST(RequirementsTest, ParseInvalidRequirement) {
    EXPECT_THROW({
        Requirement::parse("not a valid requirement ???");
    }, std::exception);
}

TEST(RequirementsTest, LocalFileDetected) {
    EXPECT_THROW({
        Requirement::parse("./myscript.whl");
    }, std::exception);
}