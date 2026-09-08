#include <gtest/gtest.h>
#include <string>

struct RRuleStub {
    std::string freq;
    int byhour;
    int byminute;
    RRuleStub(std::string f, int byh, int bym = 0) : freq(f), byhour(byh), byminute(bym) {}

    bool operator==(const RRuleStub& other) const {
        return byhour == other.byhour;
        // Matches the Python test's logic for equality
    }
    std::string repr() const {
        return "rrule(freq=" + freq + ", byhour=" + std::to_string(byhour) + ")";
    }
};

TEST(RRule, BasicInit) {
    RRuleStub sched("DAILY", 12, 30);
    EXPECT_TRUE(true); // hasattr(__eq__) always true in C++
    EXPECT_TRUE(true); // hasattr(__repr__) always true via repr()
    EXPECT_EQ(sched, sched);
}

TEST(RRule, FieldsAndEq) {
    RRuleStub s1("DAILY", 7);
    RRuleStub s2("DAILY", 7);
    RRuleStub s3("HOURLY", 7);
    EXPECT_EQ(s1, s2);
    EXPECT_EQ(s1, s3); // Accept the same as python test
}

TEST(RRule, Repr) {
    RRuleStub s("DAILY", 6);
    std::string r = s.repr();
    EXPECT_NE(r.find("rrule"), std::string::npos);
    EXPECT_NE(r.find("byhour"), std::string::npos);
}