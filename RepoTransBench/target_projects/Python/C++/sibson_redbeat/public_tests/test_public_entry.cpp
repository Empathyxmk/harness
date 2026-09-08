#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <string>
#include <memory>
#include <ctime>
#include <stdexcept>

struct AppStub {
    std::string redbeat_conf_key_prefix = "redbeat:";
    std::string redbeat_conf_schedule_key = "redbeat::schedule";
    struct RedisStub {
        nlohmann::json stored_value;
        int called_zrank = 0;
        int called_zscore = 0;
        std::string exists_key;
        bool exists_ret = false;
        std::string hget_key;
        std::string hget_field;
        nlohmann::json hget_val;
        bool exists(const std::string& key) {
            exists_key = key;
            return exists_ret;
        }
        nlohmann::json hget(const std::string& key, const std::string& field) {
            hget_key = key; hget_field = field;
            return hget_val;
        }
        int zrank(const std::string&, const std::string&) { return 0; }
        int zscore(const std::string&, const std::string&) { return 789; }
    };
    RedisStub* redbeat_redis_obj = new RedisStub;
    RedisStub* redbeat_redis_fn() { return redbeat_redis_obj; }
    ~AppStub() { delete redbeat_redis_obj; }
};

struct RedBeatSchedulerEntry {
    std::string name;
    std::string task;
    nlohmann::json schedule;
    std::string key;
    int score;
    int total_run_count;
    std::tm last_run_at = {};
    RedBeatSchedulerEntry(const std::string& name_ = "public_test", const std::string& task_ = "tasks.public_test") :
        name(name_), task(task_), score(888), total_run_count(0)
    { }
    void save() {}
    void delete_() {}
    std::string generate_key(const std::string& app, const std::string& nm) { return "redbeat:" + nm; }
    RedBeatSchedulerEntry next(bool only_update_last_run_at = false) { return *this; }
    static RedBeatSchedulerEntry from_key(const std::string& k, const AppStub&) {
        if (k == "doesnotexist_public") throw std::out_of_range("KeyError");
        return RedBeatSchedulerEntry();
    }
};

class PublicRedBeatEntryTest : public ::testing::Test {
protected:
    AppStub app;
    RedBeatSchedulerEntry create_entry() {
        return RedBeatSchedulerEntry();
    }
};

TEST_F(PublicRedBeatEntryTest, BasicSave) {
    RedBeatSchedulerEntry e = create_entry();
    e.save();

    nlohmann::json expected = {
        {"name", "public_test"},
        {"task", "tasks.public_test"},
        {"schedule", e.schedule},
        {"args", nlohmann::json()},
        {"kwargs", nlohmann::json()},
        {"options", nlohmann::json()},
        {"enabled", true}
    };

    std::string expected_key = app.redbeat_conf_key_prefix + "public_test";
    auto* redis = app.redbeat_redis_fn();
    redis->hget_val = expected;
    EXPECT_EQ(expected, redis->hget(expected_key, "definition"));
    EXPECT_EQ(0, redis->zrank(app.redbeat_conf_schedule_key, e.key));
    EXPECT_EQ(789, redis->zscore(app.redbeat_conf_schedule_key, e.key));
}