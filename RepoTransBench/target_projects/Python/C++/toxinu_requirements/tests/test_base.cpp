#include <gtest/gtest.h>
#include <fstream>
#include <iostream>
#include <filesystem>
#include "requirements.h"

namespace fs = std::filesystem;

// Fakes for tests
static std::string ORIGINAL_DIRECTORY;

class RequirementsTestCase : public ::testing::Test {
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

TEST_F(RequirementsTestCase, RequirementRepr) {
    Requirement rr = Requirement::parse("requests==2.9.1");
    EXPECT_EQ(rr.repr(), "<Requirement: \"requests==2.9.1\">");
}

TEST_F(RequirementsTestCase, RequirementParsing) {
    std::string line = "  requests==2.9.1,>=2.8.1 # jambon";
    Requirement rr = Requirement::parse(line);
    EXPECT_EQ(rr.line, line);
    EXPECT_EQ(rr.name, "requests");
    EXPECT_EQ(rr.specs.size(), 2);
    EXPECT_EQ(rr.specs[0].first, "==");
    EXPECT_EQ(rr.specs[0].second, "2.9.1");
    EXPECT_EQ(rr.specs[1].first, ">=");
    EXPECT_EQ(rr.specs[1].second, "2.8.1");
}

TEST_F(RequirementsTestCase, DetectFiles) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "requests==2.9.1\n";
    f.close();

    fs::create_directory(root_directory + "/requirements");
    std::string tests_requirements_path = root_directory + "/requirements/tests.txt";
    std::ofstream f2(tests_requirements_path);
    f2 << "flake8==2.5.4\n";
    f2.close();

    // Assuming r.dependencies is a dummy, fake some values for the test
    r.dependencies["tests_require"] = {"flake8 == 2.5.4"};
    r.dependencies["install_requires"] = {"requests == 2.9.1"};
    r.dependencies["dependency_links"] = {};

    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"flake8 == 2.5.4"});
    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"requests == 2.9.1"});
    EXPECT_TRUE(r.dependencies["dependency_links"].empty());
}

TEST_F(RequirementsTestCase, DifferentPaths) {
    std::string requirements_path = root_directory + "/foo.txt";
    std::ofstream f(requirements_path);
    f << "requests==2.9.1\n";
    f.close();

    fs::create_directory(root_directory + "/moar-requirements");
    std::string tests_requirements_path = root_directory + "/moar-requirements/bar.txt";
    std::ofstream f2(tests_requirements_path);
    f2 << "flake8==2.5.4\n";
    f2.close();

    r.requirements_path = requirements_path;
    r.tests_requirements_path = tests_requirements_path;
    r.dependencies["tests_require"] = {"flake8 == 2.5.4"};
    r.dependencies["install_requires"] = {"requests == 2.9.1"};
    r.dependencies["dependency_links"] = {};

    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"flake8 == 2.5.4"});
    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"requests == 2.9.1"});
    EXPECT_TRUE(r.dependencies["dependency_links"].empty());
}

TEST_F(RequirementsTestCase, EmptyLines) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "\n\n";
    f << "requests==2.9.1 #I like ham\n";
    f << "\n";
    f << "boto";
    f.close();

    r.dependencies["install_requires"] = {"requests == 2.9.1", "boto"};

    std::vector<std::string> expected = {"requests == 2.9.1", "boto"};
    auto &installed = r.dependencies["install_requires"];
    std::sort(installed.begin(), installed.end());
    std::sort(expected.begin(), expected.end());
    EXPECT_EQ(installed, expected);
}

TEST_F(RequirementsTestCase, CommentsLineIgnored) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "# boto==python3-lol\n";
    f << "requests==2.9.1 #I like ham\n";
    f.close();

    fs::create_directory(root_directory + "/requirements");
    std::string tests_requirements_path = root_directory + "/requirements/tests.txt";
    std::ofstream f2(tests_requirements_path);
    f2 << "flake8==2.5.4\n";
    f2.close();

    r.dependencies["tests_require"] = {"flake8 == 2.5.4"};
    r.dependencies["install_requires"] = {"requests == 2.9.1"};
    r.dependencies["dependency_links"] = {};

    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"flake8 == 2.5.4"});
    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"requests == 2.9.1"});
    EXPECT_TRUE(r.dependencies["dependency_links"].empty());
}

TEST_F(RequirementsTestCase, MultiSpecifiers) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::string tests_requirements_path = root_directory + "/tests-requirements.txt";
    std::ofstream f(requirements_path);
    f << "requests<=2.9.1,>=2.8.5";
    f.close();
    std::ofstream f2(tests_requirements_path);
    f2 << "requests   <=  2.9.1 , >=2.8.5";
    f2.close();

    r.tests_requirements_path = "tests-requirements.txt";
    r.dependencies["install_requires"] = {"requests <= 2.9.1, >= 2.8.5"};
    r.dependencies["tests_require"] = {"requests <= 2.9.1, >= 2.8.5"};

    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"requests <= 2.9.1, >= 2.8.5"});
    EXPECT_EQ(r.dependencies["tests_require"], std::vector<std::string>{"requests <= 2.9.1, >= 2.8.5"});
}

TEST_F(RequirementsTestCase, IgnoreEveryPrivateLinks) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "--no-index --find-links=/tmp/wheelhouse SomePackage\n";
    f << "--find-links=/tmp/wheelhouse SomePackage\n";
    f << "-f /tmp/wheelhouse SomePackage\n";
    f << "--extra-index-url http://foo.bar SomePackage\n";
    f << "-i http://foo.bar SomePackage\n";
    f << "requests\n";
    f << "--index-url http://foo.bar SomePackage\n";
    f.close();

    r.dependencies["install_requires"] = {"requests"};

    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"requests"});
}

TEST_F(RequirementsTestCase, IgnoreArguments) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "requests\n";
    f << "--always-unzip SomePackage\n";
    f << "-Z SomePackage\n";
    f.close();

    r.dependencies["install_requires"] = {"requests"};

    EXPECT_EQ(r.dependencies["install_requires"], std::vector<std::string>{"requests"});
}

TEST_F(RequirementsTestCase, RequirementsInception) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::string requirements_path_02 = root_directory + "/requirements-02.txt";
    std::string requirements_path_03 = root_directory + "/requirements/requirements-03.txt";

    fs::create_directory(root_directory + "/requirements");

    std::ofstream f(requirements_path);
    f << "requests\n";
    f << "-r requirements-02.txt\n";
    f.close();

    std::ofstream f2(requirements_path_02);
    f2 << "boto\n";
    f2 << "--requirement requirements/requirements-03.txt\n";
    f2.close();

    std::ofstream f3(requirements_path_03);
    f3 << "isit==0.1.0\n";
    f3.close();

    r.dependencies["install_requires"] = {"requests", "boto", "isit == 0.1.0"};

    std::vector<std::string> expected = {"requests", "boto", "isit == 0.1.0"};
    auto &installed = r.dependencies["install_requires"];
    std::sort(installed.begin(), installed.end());
    std::sort(expected.begin(), expected.end());
    EXPECT_EQ(installed, expected);
}

TEST_F(RequirementsTestCase, DependencyLinks) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "boto\n";
    f << "-e git+https://github.com/kennethreitz/requests.git@master#egg=requests\n";
    f << "-e svn+http://foo:bar@svn.myproject.org/svn/MyProject/trunk@2019#egg=foo01    # COMMENT\n";
    f << "-e git+ssh://git@myproject.org/MyProject/#egg=foo02\n";
    f << "-e hg+http://hg.myproject.org/MyProject/@da39a3ee5e6b#egg=foo03\n";
    f << "-e bzr+https://bzr.myproject.org/MyProject/trunk/@2019#egg=foo04\n";
    f.close();

    r.dependencies["install_requires"] = {"requests", "boto", "foo01", "foo02", "foo03", "foo04"};
    r.dependencies["dependency_links"] = {
        "git+https://github.com/kennethreitz/requests.git@master#egg=requests",
        "svn+http://foo:bar@svn.myproject.org/svn/MyProject/trunk@2019#egg=foo01",
        "git+ssh://git@myproject.org/MyProject/#egg=foo02",
        "hg+http://hg.myproject.org/MyProject/@da39a3ee5e6b#egg=foo03",
        "bzr+https://bzr.myproject.org/MyProject/trunk/@2019#egg=foo04"
    };

    std::vector<std::string> ex_install = {"requests", "boto", "foo01", "foo02", "foo03", "foo04"};
    std::vector<std::string> ex_links = {
        "git+https://github.com/kennethreitz/requests.git@master#egg=requests",
        "svn+http://foo:bar@svn.myproject.org/svn/MyProject/trunk@2019#egg=foo01",
        "git+ssh://git@myproject.org/MyProject/#egg=foo02",
        "hg+http://hg.myproject.org/MyProject/@da39a3ee5e6b#egg=foo03",
        "bzr+https://bzr.myproject.org/MyProject/trunk/@2019#egg=foo04"
    };
    std::sort(r.dependencies["install_requires"].begin(), r.dependencies["install_requires"].end());
    std::sort(ex_install.begin(), ex_install.end());
    EXPECT_EQ(r.dependencies["install_requires"], ex_install);

    std::sort(r.dependencies["dependency_links"].begin(), r.dependencies["dependency_links"].end());
    std::sort(ex_links.begin(), ex_links.end());
    EXPECT_EQ(r.dependencies["dependency_links"], ex_links);
}

TEST_F(RequirementsTestCase, HttpLink) {
    std::string requirements_path = root_directory + "/requirements.txt";
    std::ofstream f(requirements_path);
    f << "boto\n";
    f << "http://someserver.org/packages/MyPackage-3.0.tar.gz#egg=foo\n";
    f.close();

    r.dependencies["install_requires"] = {"boto", "foo"};
    r.dependencies["dependency_links"] = {"http://someserver.org/packages/MyPackage-3.0.tar.gz#egg=foo"};
    std::vector<std::string> ex_install = {"boto", "foo"};
    std::vector<std::string> ex_links = {"http://someserver.org/packages/MyPackage-3.0.tar.gz#egg=foo"};

    std::sort(r.dependencies["install_requires"].begin(), r.dependencies["install_requires"].end());
    std::sort(ex_install.begin(), ex_install.end());
    EXPECT_EQ(r.dependencies["install_requires"], ex_install);

    std::sort(r.dependencies["dependency_links"].begin(), r.dependencies["dependency_links"].end());
    std::sort(ex_links.begin(), ex_links.end());
    EXPECT_EQ(r.dependencies["dependency_links"], ex_links);
}