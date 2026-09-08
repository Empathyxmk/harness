#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <chrono>
#include <ctime>
#include <string>

struct Schedule {
    int run_every;
    bool relative;
    Schedule(int re, bool rel = false) : run_every(re), relative(rel) {}
};

struct Crontab {
    std::string hour;
    Crontab(const std::string& h = "*") : hour(h) {}
    std::string _orig_hour() const { return hour; }
};
struct RedBeatJSONEncoder {};
struct RedBeatJSONDecoder {};

class PublicRedBeatJSONEncoderTest : public ::testing::Test {
protected:
    nlohmann::json dumps(const Schedule& obj) {
        nlohmann::json j;
        j["type"] = "schedule";
        j["run_every"] = obj.run_every;
        j["relative"] = obj.relative;
        return j;
    }
    Schedule loads(const nlohmann::json& j) {
        return Schedule(j["run_every"], j.value("relative", false));
    }
    nlohmann::json dumps(const Crontab& obj) {
        nlohmann::json j;
        j["type"] = "crontab";
        j["hour"] = obj.hour;
        return j;
    }
    Crontab loads_crontab(const nlohmann::json& j) {
        return Crontab(j.value("hour", "*"));
    }
};

TEST_F(PublicRedBeatJSONEncoderTest, Schedule) {
    Schedule s(5);
    nlohmann::json dumped = dumps(s);
    Schedule loaded = loads(dumped);
    EXPECT_EQ(loaded.run_every, 5);
}

TEST_F(PublicRedBeatJSONEncoderTest, Crontab) {
    Crontab c("3");
    nlohmann::json dumped = dumps(c);
    Crontab loaded = loads_crontab(dumped);
    EXPECT_EQ(loaded.hour, "3");
    EXPECT_EQ(loaded._orig_hour(), "3");
}

TEST_F(PublicRedBeatJSONEncoderTest, DateTime) {
    nlohmann::json dumped;
    dumped["type"] = "datetime";
    dumped["year"] = 2020;
    dumped["month"] = 6;
    dumped["day"] = 15;
    nlohmann::json loaded = dumped;
    EXPECT_EQ(loaded["year"], 2020);
}

TEST(PublicRedBeatJSONEncoderStandalone, WeekdayEncodeDecodePublic) {
    int weekday = 2;
    nlohmann::json dumped = weekday;
    int loaded = dumped;
    EXPECT_EQ(loaded, 2);
}

TEST(PublicRedBeatJSONEncoderStandalone, ScheduleRelativePublic) {
    Schedule s(10, true);
    nlohmann::json dumped;
    dumped["type"] = "schedule";
    dumped["run_every"] = s.run_every;
    dumped["relative"] = s.relative;
    Schedule loaded(dumped["run_every"], dumped["relative"]);
    EXPECT_TRUE(loaded.relative);
    EXPECT_EQ(loaded.run_every, 10);
}