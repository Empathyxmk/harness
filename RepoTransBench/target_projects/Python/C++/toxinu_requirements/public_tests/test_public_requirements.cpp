#include <gtest/gtest.h>
#include "requirements.h"

TEST(PublicRequirementsTest, ParseNormalRequirementPublic) {
    Requirement r = Requirement::parse("boto3>=1.15");
    ASSERT_FALSE(r.name.empty());
    EXPECT_EQ(r.name, "boto3");
    EXPECT_FALSE(r.specifier.empty());
    EXPECT_FALSE(r.is_local_file);
}

TEST(PublicRequirementsTest, ParseLocalFileEditablePublic) {
    EXPECT_THROW({
        Requirement::parse("/another/path/to/pkg2", true);
    }, std::exception);
}

TEST(PublicRequirementsTest, ParseLocalFileSchemePublic) {
    Requirement r = Requirement::parse("file:///tmp/anotherpackage#egg=otherpkg");
    EXPECT_NE(r.line.find("file://"), std::string::npos);
}

TEST(PublicRequirementsTest, ParseVcsUrlPublic) {
    std::string vcs_url = "hg+https://bitbucket.org/user/repo2#egg=hgproject";
    Requirement r = Requirement::parse(vcs_url);
    std::string s = r.line;
    EXPECT_TRUE(s.rfind("hg+", 0) == 0 || s.find("hg+") != std::string::npos);
}

TEST(PublicRequirementsTest, ParseWithMarkerPublic) {
    Requirement r = Requirement::parse("urllib3; sys_platform==\"win32\"");
    ASSERT_FALSE(r.name.empty());
    EXPECT_FALSE(r.marker.empty());
}

TEST(PublicRequirementsTest, StrReprPublic) {
    Requirement r = Requirement::parse("sqlalchemy");
    std::string s = r.str();
    std::string rep = r.repr();
    EXPECT_TRUE(s == "sqlalchemy" || s == "<Requirement: \"sqlalchemy\">");
    EXPECT_FALSE(rep.empty());
}

TEST(PublicRequirementsTest, EqualityAndHashPublic) {
    Requirement r1 = Requirement::parse("bar==3.4");
    Requirement r2 = Requirement::parse("bar==3.4");
    try {
        EXPECT_TRUE(r1 == r2);
    } catch (...) {}
    (void)r1.hash();
    (void)r2.hash();
}

TEST(PublicRequirementsTest, RequirementExtrasPublic) {
    Requirement r = Requirement::parse("pandas[performance,io]>=1.0");
    EXPECT_FALSE(r.extras.empty());
    EXPECT_NE(std::find(r.extras.begin(), r.extras.end(), "performance"), r.extras.end());
}

TEST(PublicRequirementsTest, ParseInvalidRequirementPublic) {
    EXPECT_THROW({
        Requirement::parse("??? this is not valid");
    }, std::exception);
}

TEST(PublicRequirementsTest, LocalFileDetectedPublic) {
    EXPECT_THROW({
        Requirement::parse("../something.whl");
    }, std::exception);
}