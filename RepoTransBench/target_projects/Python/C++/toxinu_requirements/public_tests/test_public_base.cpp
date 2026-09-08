#include <gtest/gtest.h>
#include <fstream>
#include <iostream>
#include <filesystem>
#include "requirements.h"

namespace fs = std::filesystem;

static std::string ORIGINAL_DIRECTORY;

class RequirementsPublicTestCase : public ::testing::Test {
protected:
    std::string root_directory;
    Requirements r;

    virtual void SetUp() override {
        ORIGINAL_DIRECTORY = fs::current_path().string();
        root_directory = fs::temp_directory_path() / fs::unique_path().string();
        fs::create_directory(root_directory);
        fs::current_path(root_directory);
        r = Requirements();
    }

    virtual void TearDown() override {
        fs::current_path(ORIGINAL_DIRECTORY);
        fs::remove_all(root_directory);
    }
};

TEST_F(RequirementsPublicTestCase, RequirementReprPublic) {
    Requirement rr = Requirement::parse("pandas==1.3.1");
    EXPECT_EQ(rr.repr(), "<Requirement: \"pandas==1.3.1\">");
}

TEST_F(RequirementsPublicTestCase, RequirementParsingPublic) {
    std::string line = "  pandas==1.3.1,>=1.0.0 # cheese";
    Requirement rr = Requirement::parse(line);
    EXPECT_EQ(rr.line, line);
    EXPECT_EQ(rr.name, "pandas");
    EXPECT_EQ(rr.specs.size(), 2);
    EXPECT_EQ(rr.specs[0].first, "==");
    EXPECT_EQ(rr.specs[0].second, "1.3.1");
    EXPECT_EQ(rr.specs[1].first, ">=");
    EXPECT_EQ(rr.specs[1].second, "1.0.0");
}

TEST_F(RequirementsPublicTestCase, DetectFilesPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "pandas==1.3.1\n";
    f.close();

    fs::create_directory(root_directory + "/requirements");
    std::string tests_requirements_path = root_directory + "/requirements/tests.txt";
    std::ofstream f2(tests_requirements_path);
    f2 << "pytest==6.2.5\n";
    f2.close();

    r.dependencies["tests_require"] = {"pytest == 6.2.5"};
    r.dependencies["install_requires"] = {"pandas == 1.3.1"};
    r.dependencies["dependency_links"] = {};

    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"pytest == 6.2.5"});
    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"pandas == 1.3.1"});
    EXPECT_TRUE(r.dependencies["dependency_links"].empty());
}

TEST_F(RequirementsPublicTestCase, DifferentPathsPublic) {
    std::string requirements_path = root_directory + "/reqs.txt";
    std::ofstream f(requirements_path);
    f << "pandas==1.3.1\n";
    f.close();

    fs::create_directory(root_directory + "/other-requirements");
    std::string tests_requirements_path = root_directory + "/other-requirements/baz.txt";
    std::ofstream f2(tests_requirements_path);
    f2 << "pytest==6.2.5\n";
    f2.close();

    r.requirements_path = requirements_path;
    r.tests_requirements_path = tests_requirements_path;
    r.dependencies["tests_require"] = {"pytest == 6.2.5"};
    r.dependencies["install_requires"] = {"pandas == 1.3.1"};
    r.dependencies["dependency_links"] = {};

    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"pytest == 6.2.5"});
    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"pandas == 1.3.1"});
    EXPECT_TRUE(r.dependencies["dependency_links"].empty());
}

TEST_F(RequirementsPublicTestCase, EmptyLinesPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "\n\n";
    f << "pandas==1.3.1 #I like cheese\n";
    f << "\n";
    f << "numpy";
    f.close();

    r.dependencies["install_requires"] = {"pandas == 1.3.1", "numpy"};
    std::vector<std::string> expected = {"pandas == 1.3.1", "numpy"};
    auto &installed = r.dependencies["install_requires"];
    std::sort(installed.begin(), installed.end());
    std::sort(expected.begin(), expected.end());
    EXPECT_EQ(installed, expected);
}

TEST_F(RequirementsPublicTestCase, CommentsLineIgnoredPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "# numpy==python3-bar\n";
    f << "pandas==1.3.1 #I like cheese\n";
    f.close();

    fs::create_directory(root_directory + "/requirements");
    std::string tests_requirements_path = root_directory + "/requirements/tests.txt";
    std::ofstream f2(tests_requirements_path);
    f2 << "pytest==6.2.5\n";
    f2.close();

    r.dependencies["tests_require"] = {"pytest == 6.2.5"};
    r.dependencies["install_requires"] = {"pandas == 1.3.1"};
    r.dependencies["dependency_links"] = {};

    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"pytest == 6.2.5"});
    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"pandas == 1.3.1"});
    EXPECT_TRUE(r.dependencies["dependency_links"].empty());
}

TEST_F(RequirementsPublicTestCase, MultiSpecifiersPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::string tests_requirements_path = root_directory + "/tests-extra-requirements.txt";
    std::ofstream f(requirements_path);
    f << "pandas<=1.3.1,>=1.0.5";
    f.close();
    std::ofstream f2(tests_requirements_path);
    f2 << "pandas   <=  1.3.1 , >=1.0.5";
    f2.close();

    r.tests_requirements_path = "tests-extra-requirements.txt";
    r.dependencies["install_requires"] = {"pandas <= 1.3.1, >= 1.0.5"};
    r.dependencies["tests_require"] = {"pandas <= 1.3.1, >= 1.0.5"};

    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"pandas <= 1.3.1, >= 1.0.5"});
    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"pandas <= 1.3.1, >= 1.0.5"});
}

TEST_F(RequirementsPublicTestCase, IgnoreEveryPrivateLinksPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "--no-index --find-links=/tmp/otherwheel SomeOtherPkg\n";
    f << "--find-links=/tmp/otherwheel AnotherPkg\n";
    f << "-f /tmp/otherwheel YetAnotherPkg\n";
    f << "--extra-index-url http://baz.qux SomePkg\n";
    f << "-i http://baz.qux TestPkg\n";
    f << "pandas\n";
    f << "--index-url http://baz.qux OrphanPkg\n";
    f.close();

    r.dependencies["install_requires"] = {"pandas"};

    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"pandas"});
}

TEST_F(RequirementsPublicTestCase, IgnoreArgumentsPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "pandas\n";
    f << "--always-unzip AnotherPackage\n";
    f << "-Z YetAnotherPackage\n";
    f.close();

    r.dependencies["install_requires"] = {"pandas"};

    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"pandas"});
}

TEST_F(RequirementsPublicTestCase, RequirementsInceptionPublic) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::string requirements_path_02 = root_directory + "/requirements-04.txt";
    std::string requirements_path_03 = root_directory + "/requirements/requirements-05.txt";

    fs::create_directory(root_directory + "/requirements");

    std::ofstream f(requirements_path);
    f << "pandas\n";
    f << "-r requirements-04.txt\n";
    f.close();

    std::ofstream f2(requirements_path_02);
    f2 << "numpy\n";
    f2 << "--requirement requirements/requirements-05.txt\n";
    f2.close();

    std::ofstream f3(requirements_path_03);
    f3 << "requests==2.25.1\n";
    f3.close();

    r.dependencies["install_requires"] = {"pandas", "numpy", "requests == 2.25.1"};

    std::vector<std::string> expected = {"pandas", "numpy", "requests == 2.25.1"};
    auto &installed = r.dependencies["install_requires"];
    std::sort(installed.begin(), installed.end());
    std::sort(expected.begin(), expected.end());
    EXPECT_EQ(installed, expected);
}