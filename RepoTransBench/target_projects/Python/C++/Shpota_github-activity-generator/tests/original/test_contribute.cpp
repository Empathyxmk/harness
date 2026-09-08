#include <gtest/gtest.h>
#include "contribute.h"
#include <filesystem>
#include <fstream>
#include <cstdio>

using namespace std::chrono;

// Helper to delete test repos before/after each test
void cleanup_repos() {
    std::string cwd = std::filesystem::current_path().string();
    for (auto& d : std::filesystem::directory_iterator(cwd)) {
        if (d.is_directory() && d.path().filename().string().rfind("repository-",0) == 0) {
            std::filesystem::remove_all(d);
        }
    }
}

class ContributeTest : public ::testing::Test {
protected:
    void SetUp() override { cleanup_repos(); }
    void TearDown() override { cleanup_repos(); }
};

TEST_F(ContributeTest, MessageAndContributionsPerDayBounds) {
    auto now = system_clock::now();
    std::string msg = message(now);
    ASSERT_NE(msg.find("Contribution"), std::string::npos);

    // Max commits capped at 20
    Args args;
    args.max_commits = 50;
    ASSERT_EQ(contributions_per_day(args, 50), 20);

    // Min commits floored at 1
    args.max_commits = -5;
    ASSERT_EQ(contributions_per_day(args, -5), 1);
}

TEST_F(ContributeTest, ArgumentsAndInvalidArgs) {
    std::vector<std::string> argv = {
        "--no_weekends", "--max_commits", "4",
        "--frequency", "50", "--days_before", "3",
        "--days_after", "1"
    };
    Args out = arguments(argv);
    ASSERT_TRUE(out.no_weekends);
    ASSERT_EQ(out.max_commits, 4);
    ASSERT_EQ(out.frequency, 50);
    ASSERT_EQ(out.days_before, 3);
    ASSERT_EQ(out.days_after, 1);

    // Invalid flag
    bool expect_exit = false;
    try {
        arguments({ "--notarealarg" }, &expect_exit);
        FAIL() << "Expected exception for unknown argument";
    } catch (std::runtime_error& ex) {
        ASSERT_TRUE(expect_exit);
        ASSERT_NE(std::string(ex.what()).find("SystemExit"), std::string::npos);
    }
}

TEST_F(ContributeTest, MainNegativeDays) {
    // main should fail with negative days_before or days_after
    bool expect_exit = false;
    try {
        main_entry({ "--days_before", "-2" }, &expect_exit);
        FAIL() << "Expected runtime_error";
    } catch (std::runtime_error& ex) {
        ASSERT_TRUE(expect_exit);
        ASSERT_NE(std::string(ex.what()).find("must not be negative"), std::string::npos);
    }
    expect_exit = false;
    try {
        main_entry({ "--days_after", "-2" }, &expect_exit);
        FAIL() << "Expected runtime_error";
    } catch (std::runtime_error& ex) {
        ASSERT_TRUE(expect_exit);
        ASSERT_NE(std::string(ex.what()).find("must not be negative"), std::string::npos);
    }
}

TEST_F(ContributeTest, RunAndContribute) {
    // Test contribute() writing to README.md
    std::string test_dir = "repository-test-dir";
    std::filesystem::create_directory(test_dir);
    auto dt = system_clock::from_time_t(
        std::mktime(new std::tm{0,45,15,17,1,123/*2023-2-17 15:45:00*/})
    );
    contribute(dt, test_dir);
    std::ifstream ifs(test_dir + "/README.md");
    ASSERT_TRUE(ifs.is_open());
    std::string content;
    std::getline(ifs, content);
    ASSERT_NE(content.find("Contribution:"), std::string::npos);
    ifs.close();
    std::filesystem::remove_all(test_dir);
}

TEST_F(ContributeTest, MainMinimal) {
    // Simulate minimal main run (no error should be thrown)
    bool expect_exit = false;
    main_entry({ "--days_before", "1", "--days_after", "1", "--max_commits", "1" }, &expect_exit);
    ASSERT_FALSE(expect_exit);
}

TEST_F(ContributeTest, MainWithRepository) {
    // Provide repository, user, email
    bool expect_exit = false;
    main_entry({
        "--repository", "https://github.com/testuser/somerepo.git",
        "--user_name", "foo", "--user_email", "bar@test.com",
        "--days_before", "1", "--days_after", "1"
    }, &expect_exit);
    ASSERT_FALSE(expect_exit);
}