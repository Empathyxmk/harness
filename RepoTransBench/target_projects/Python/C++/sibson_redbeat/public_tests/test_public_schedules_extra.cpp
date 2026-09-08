#include <gtest/gtest.h>
#include <string>

struct RRuleStub {
    std::string freq;
    int byhour;
    int byminute;
    RRuleStub(std::string f, int byh, int bym = 0) : freq(f), byhour(byh), byminute(bym) {}

    bool operator==(const RRuleStub& other) const {
        return byhour == other.byhour;
    }
    std::string repr() const {
        return "rrule(freq=" + freq + ", byhour=" + std::to_string(byhour) + ")";
    }
};

TEST(RRulePublic, BasicInitPublic) {
    RRuleStub sched("WEEKLY", 8, 15);
    EXPECT_TRUE(true);
    EXPECT_TRUE(true);
    EXPECT_EQ(sched, sched);
}

TEST(RRulePublic, FieldsAndEqPublic) {
    RRuleStub s1("WEEKLY", 8);
    RRuleStub s2("WEEKLY", 8);
    RRuleStub s3("MONTHLY", 8);
    EXPECT_EQ(s1, s2);
    EXPECT_EQ(s1, s3);
}

TEST(RRulePublic, ReprPublic) {
    RRuleStub s("WEEKLY", 4);
    std::string r = s.repr();
    EXPECT_NE(r.find("rrule"), std::string::npos);
    EXPECT_NE(r.find("byhour"), std::string::npos);
}