#include <gtest/gtest.h>
#include <regex>
#include <string>
#include <map>
#include <cmath>

#include "pytimeparse/timeparse.h"

// Helper function to compare two maps by value equality
template <typename K, typename V>
bool map_eq(const std::map<K, V>& a, const std::map<K, V>& b) {
    return a == b;
}

class TestTimeparse : public ::testing::Test {
protected:
    void SetUp() override {}
};

TEST_F(TestTimeparse, test_mins) {
    std::smatch match;
    std::string minutes[] = {"32min","32mins","32minute","32minutes","32mins","32min"};
    for (const auto& s : minutes) {
        ASSERT_TRUE(std::regex_match(s, match, pytimeparse::MINS));
        ASSERT_EQ(match.str("mins"), "32");
    }
}

TEST_F(TestTimeparse, test_hrs) {
    std::smatch match;
    std::vector<std::string> hour_cases = {
        "32h","32hr","32hrs","32hour","32hours","32 hours","32 h"
    };
    for (const auto& s : hour_cases) {
        ASSERT_TRUE(std::regex_match(s, match, pytimeparse::HOURS));
        ASSERT_EQ(match.str("hours"), "32");
    }
}

TEST_F(TestTimeparse, test_time) {
    std::smatch match;
    std::string expr = "16h32m64s  ";
    std::string pat = pytimeparse::TIMEFORMATS[0] + R"(\s*$)";
    ASSERT_TRUE(std::regex_match(expr, match, std::regex(pat)));
    std::map<std::string, std::string> got = {
        {"hours", match.str("hours")},
        {"mins", match.str("mins")},
        {"secs", match.str("secs")}
    };
    std::map<std::string, std::string> want = {
        {"hours","16"}, {"mins","32"}, {"secs","64"}
    };
    for (const auto& kv : want)
        ASSERT_EQ(got[kv.first], kv.second);
}

TEST_F(TestTimeparse, test_timeparse_multipliers) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("32 min"), 1920);
    ASSERT_EQ(timeparse("1 min"), 60);
    ASSERT_EQ(timeparse("1 hours"), 3600);
    ASSERT_EQ(timeparse("1 day"), 86400);
    ASSERT_EQ(timeparse("1 sec"), 1);
}

TEST_F(TestTimeparse, test_timeparse_signs) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("+32 m 1 s"), 1921);
    ASSERT_EQ(timeparse("+ 32 m 1 s"), 1921);
    ASSERT_EQ(timeparse("-32 m 1 s"), -1921);
    ASSERT_EQ(timeparse("- 32 m 1 s"), -1921);
    ASSERT_EQ(timeparse("32 m - 1 s"), std::nullopt);
    ASSERT_EQ(timeparse("32 m + 1 s"), std::nullopt);
}

TEST_F(TestTimeparse, test_timeparse_1) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("32m"), 1920);
    ASSERT_EQ(timeparse("+32m"), 1920);
    ASSERT_EQ(timeparse("-32m"), -1920);
}

TEST_F(TestTimeparse, test_timeparse_2) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("2h32m"), 9120);
    ASSERT_EQ(timeparse("+2h32m"), 9120);
    ASSERT_EQ(timeparse("-2h32m"), -9120);
}

TEST_F(TestTimeparse, test_timeparse_3) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("3d2h32m"), 268320);
    ASSERT_EQ(timeparse("+3d2h32m"), 268320);
    ASSERT_EQ(timeparse("-3d2h32m"), -268320);
}

TEST_F(TestTimeparse, test_timeparse_4) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1w3d2h32m"), 873120);
    ASSERT_EQ(timeparse("+1w3d2h32m"), 873120);
    ASSERT_EQ(timeparse("-1w3d2h32m"), -873120);
}

TEST_F(TestTimeparse, test_timeparse_5) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1w 3d 2h 32m"), 873120);
    ASSERT_EQ(timeparse("+1w 3d 2h 32m"), 873120);
    ASSERT_EQ(timeparse("-1w 3d 2h 32m"), -873120);
}

TEST_F(TestTimeparse, test_timeparse_6) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1 w 3 d 2 h 32 m"), 873120);
    ASSERT_EQ(timeparse("+1 w 3 d 2 h 32 m"), 873120);
    ASSERT_EQ(timeparse("-1 w 3 d 2 h 32 m"), -873120);
}

TEST_F(TestTimeparse, test_timeparse_7) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("4:13"), 253);
    ASSERT_EQ(timeparse("+4:13"), 253);
    ASSERT_EQ(timeparse("-4:13"), -253);
}

TEST_F(TestTimeparse, test_timeparse_bare_seconds) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse(":13"), 13);
    ASSERT_EQ(timeparse("+:13"), 13);
    ASSERT_EQ(timeparse("-:13"), -13);
}

TEST_F(TestTimeparse, test_timeparse_8) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("4:13:02"), 15182);
    ASSERT_EQ(timeparse("+4:13:02"), 15182);
    ASSERT_EQ(timeparse("-4:13:02"), -15182);
}

TEST_F(TestTimeparse, test_timeparse_9) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("4:13:02.266").value(), 15182.266, 1e-5);
    ASSERT_NEAR(timeparse("+4:13:02.266").value(), 15182.266, 1e-5);
    ASSERT_NEAR(timeparse("-4:13:02.266").value(), -15182.266, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_10) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("2:04:13:02.266").value(), 187982.266, 1e-5);
    ASSERT_NEAR(timeparse("+2:04:13:02.266").value(), 187982.266, 1e-5);
    ASSERT_NEAR(timeparse("-2:04:13:02.266").value(), -187982.266, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_granularity_1) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("4:32", "minutes"), 272*60);
    ASSERT_EQ(timeparse("+4:32", "minutes"), 272*60);
    ASSERT_EQ(timeparse("-4:32", "minutes"), -272*60);
}

TEST_F(TestTimeparse, test_timeparse_granularity_2) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("4:32:02", "minutes"), 272*60+2);
    ASSERT_EQ(timeparse("+4:32:02", "minutes"), 272*60+2);
    ASSERT_EQ(timeparse("-4:32:02", "minutes"), -(272*60+2));
}

TEST_F(TestTimeparse, test_timeparse_granularity_3) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("7:02.223", "minutes").value(), 7*60 + 2.223, 1e-5);
    ASSERT_NEAR(timeparse("+7:02.223", "minutes").value(), 7*60 + 2.223, 1e-5);
    ASSERT_NEAR(timeparse("-7:02.223", "minutes").value(), -(7*60 + 2.223), 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_granularity_4) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("0:02", "seconds"), 2);
    ASSERT_EQ(timeparse("+0:02", "seconds"), 2);
    ASSERT_EQ(timeparse("-0:02", "seconds"), -2);
}

TEST_F(TestTimeparse, test_timeparse_11) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("2 days,  4:13:02"), 187982);
    ASSERT_EQ(timeparse("+2 days,  4:13:02"), 187982);
    ASSERT_EQ(timeparse("-2 days,  4:13:02"), -187982);
}

TEST_F(TestTimeparse, test_timeparse_12) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("2 days,  4:13:02.266").value(), 187982.266, 1e-5);
    ASSERT_NEAR(timeparse("+2 days,  4:13:02.266").value(), 187982.266, 1e-5);
    ASSERT_NEAR(timeparse("-2 days,  4:13:02.266").value(), -187982.266, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_13) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5hr34m56s"), 20096);
    ASSERT_EQ(timeparse("+5hr34m56s"), 20096);
    ASSERT_EQ(timeparse("-5hr34m56s"), -20096);
}

TEST_F(TestTimeparse, test_timeparse_14) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5 hours, 34 minutes, 56 seconds"), 20096);
    ASSERT_EQ(timeparse("+5 hours, 34 minutes, 56 seconds"), 20096);
    ASSERT_EQ(timeparse("-5 hours, 34 minutes, 56 seconds"), -20096);
}

TEST_F(TestTimeparse, test_timeparse_15) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5 hrs, 34 mins, 56 secs"), 20096);
    ASSERT_EQ(timeparse("+5 hrs, 34 mins, 56 secs"), 20096);
    ASSERT_EQ(timeparse("-5 hrs, 34 mins, 56 secs"), -20096);
}

TEST_F(TestTimeparse, test_timeparse_16) {
    using pytimeparse::timeparse;
    ASSERT_EQ(
        timeparse("2 days, 5 hours, 34 minutes, 56 seconds"),
        192896);
    ASSERT_EQ(
        timeparse("+2 days, 5 hours, 34 minutes, 56 seconds"),
        192896);
    ASSERT_EQ(
        timeparse("-2 days, 5 hours, 34 minutes, 56 seconds"),
        -192896);
}

TEST_F(TestTimeparse, test_timeparse_16b) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("1.75 s").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("+1.75 s").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("-1.75 s").value(), -1.75, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_16c) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("1.75 sec").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("+1.75 sec").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("-1.75 sec").value(), -1.75, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_16d) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("1.75 secs").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("+1.75 secs").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("-1.75 secs").value(), -1.75, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_16e) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("1.75 second").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("+1.75 second").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("-1.75 second").value(), -1.75, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_16f) {
    using pytimeparse::timeparse;
    ASSERT_NEAR(timeparse("1.75 seconds").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("+1.75 seconds").value(), 1.75, 1e-5);
    ASSERT_NEAR(timeparse("-1.75 seconds").value(), -1.75, 1e-5);
}

TEST_F(TestTimeparse, test_timeparse_17) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1.2 m"), 72);
    ASSERT_EQ(timeparse("+1.2 m"), 72);
    ASSERT_EQ(timeparse("-1.2 m"), -72);
}

TEST_F(TestTimeparse, test_timeparse_18) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1.2 min"), 72);
    ASSERT_EQ(timeparse("+1.2 min"), 72);
    ASSERT_EQ(timeparse("-1.2 min"), -72);
}

TEST_F(TestTimeparse, test_timeparse_19) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1.2 mins"), 72);
    ASSERT_EQ(timeparse("+1.2 mins"), 72);
    ASSERT_EQ(timeparse("-1.2 mins"), -72);
}

TEST_F(TestTimeparse, test_timeparse_20) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1.2 minute"), 72);
    ASSERT_EQ(timeparse("+1.2 minute"), 72);
    ASSERT_EQ(timeparse("-1.2 minute"), -72);
}

TEST_F(TestTimeparse, test_timeparse_21) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1.2 minutes"), 72);
    ASSERT_EQ(timeparse("+1.2 minutes"), 72);
    ASSERT_EQ(timeparse("-1.2 minutes"), -72);
}

TEST_F(TestTimeparse, test_timeparse_22) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("172 hours"), 619200);
    ASSERT_EQ(timeparse("+172 hours"), 619200);
    ASSERT_EQ(timeparse("-172 hours"), -619200);
}

TEST_F(TestTimeparse, test_timeparse_23) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("172 hr"), 619200);
    ASSERT_EQ(timeparse("+172 hr"), 619200);
    ASSERT_EQ(timeparse("-172 hr"), -619200);
}

TEST_F(TestTimeparse, test_timeparse_24) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("172 h"), 619200);
    ASSERT_EQ(timeparse("+172 h"), 619200);
    ASSERT_EQ(timeparse("-172 h"), -619200);
}

TEST_F(TestTimeparse, test_timeparse_25) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("172 hrs"), 619200);
    ASSERT_EQ(timeparse("+172 hrs"), 619200);
    ASSERT_EQ(timeparse("-172 hrs"), -619200);
}

TEST_F(TestTimeparse, test_timeparse_26) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("172 hour"), 619200);
    ASSERT_EQ(timeparse("+172 hour"), 619200);
    ASSERT_EQ(timeparse("-172 hour"), -619200);
}

TEST_F(TestTimeparse, test_timeparse_27) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("1.24 days"), 107136);
    ASSERT_EQ(timeparse("+1.24 days"), 107136);
    ASSERT_EQ(timeparse("-1.24 days"), -107136);
}

TEST_F(TestTimeparse, test_timeparse_28) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5 d"), 432000);
    ASSERT_EQ(timeparse("+5 d"), 432000);
    ASSERT_EQ(timeparse("-5 d"), -432000);
}

TEST_F(TestTimeparse, test_timeparse_29) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5 day"), 432000);
    ASSERT_EQ(timeparse("+5 day"), 432000);
    ASSERT_EQ(timeparse("-5 day"), -432000);
}

TEST_F(TestTimeparse, test_timeparse_30) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5 days"), 432000);
    ASSERT_EQ(timeparse("+5 days"), 432000);
    ASSERT_EQ(timeparse("-5 days"), -432000);
}

TEST_F(TestTimeparse, test_timeparse_31) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5.6 wk"), 3386880);
    ASSERT_EQ(timeparse("+5.6 wk"), 3386880);
    ASSERT_EQ(timeparse("-5.6 wk"), -3386880);
}

TEST_F(TestTimeparse, test_timeparse_32) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5.6 week"), 3386880);
    ASSERT_EQ(timeparse("+5.6 week"), 3386880);
    ASSERT_EQ(timeparse("-5.6 week"), -3386880);
}

TEST_F(TestTimeparse, test_timeparse_33) {
    using pytimeparse::timeparse;
    ASSERT_EQ(timeparse("5.6 weeks"), 3386880);
    ASSERT_EQ(timeparse("+5.6 weeks"), 3386880);
    ASSERT_EQ(timeparse("-5.6 weeks"), -3386880);
}

// Skipped test_doctest: Python's doctest has no direct C++ equivalent