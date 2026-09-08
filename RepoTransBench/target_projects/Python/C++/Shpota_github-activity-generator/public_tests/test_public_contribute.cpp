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

class PublicContributeTest : public ::testing::Test {
protected:
    void SetUp() override { cleanup_repos(); }
    void TearDown() override { cleanup_repos(); }
};

TEST_F(PublicContributeTest, MessageAndContributionsPerDayBoundsPublic) {
    auto now = system_clock::now();
    std::string msg = message(now);
    // choose different word for check, but still checking part of the message
    ASSERT_NE(msg.find("Contr"), std::string::npos);

    // Max commits capped at 20: use large value
    Args args(false, 9999, 60);
    ASSERT_EQ(contributions_per_day(args, 9999), 20);

    // Min commits floored at 1: use a different negative
    Args args2(false, -20, 60);
    ASSERT_EQ(contributions_per_day(args2, -20), 1);
}

TEST_F(PublicContributeTest, ArgumentsAndInvalidArgsPublic) {
    std::vector<std::string> argv = {
        "--no_weekends", "--max_commits", "9", "--frequency", "10", "--days_after", "6",
        "--repository", "repo-test", "--user_name", "Public User", "--user_email", "public-user@example.com"
    };
    Args out = arguments(argv);
    ASSERT_TRUE(out.no_weekends);
    ASSERT_EQ(out.max_commits, 9);
    ASSERT_EQ(out.frequency, 10);
    ASSERT_TRUE(out.repository.has_value());
    ASSERT_EQ(out.repository.value(), "repo-test");
    ASSERT_TRUE(out.user_name.has_value());
    ASSERT_EQ(out.user_name.value(), "Public User");
    ASSERT_TRUE(out.user_email.has_value());
    ASSERT_EQ(out.user_email.value(), "public-user@example.com");
    ASSERT_EQ(out.days_after, 6);

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

TEST_F(PublicContributeTest, DatesRangePublic) {
    // different before/after numbers
    int min_day = 10;
    int max_day = 13;
    auto now = system_clock::now();
    auto justmidnight = system_clock::from_time_t(std::mktime(std::localtime(&std::chrono::system_clock::to_time_t(now))));
    auto days = dates_range(justmidnight - hours(24)*min_day, justmidnight + hours(24)*max_day);
    ASSERT_EQ(days.front().time_since_epoch(), (justmidnight - hours(24)*min_day).time_since_epoch());
    ASSERT_EQ(days.back().time_since_epoch(), (justmidnight + hours(24)*max_day).time_since_epoch());
    ASSERT_EQ(days.size(), min_day + max_day + 1);
}

TEST_F(PublicContributeTest, IsWeekendPublic) {
    // Sunday = 2023-7-9, Tuesday = 2023-7-11
    std::tm sunday_tm = {};
    sunday_tm.tm_year = 2023 - 1900; sunday_tm.tm_mon = 7 - 1; sunday_tm.tm_mday = 9;
    std::tm tuesday_tm = {};
    tuesday_tm.tm_year = 2023 - 1900; tuesday_tm.tm_mon = 7 - 1; tuesday_tm.tm_mday = 11;
    auto sunday = system_clock::from_time_t(std::mktime(&sunday_tm));
    auto tuesday = system_clock::from_time_t(std::mktime(&tuesday_tm));
    ASSERT_TRUE(is_weekend(sunday));
    ASSERT_FALSE(is_weekend(tuesday));
}