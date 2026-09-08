#include <gtest/gtest.h>
#include "dummy_logic.h"

TEST(DummyLogicTest, GroupInUserTrue) {
    DummyHost h;
    EXPECT_TRUE(h.group_in_user("docker"));
}
TEST(DummyLogicTest, GroupInUserFalse) {
    DummyHost h;
    EXPECT_FALSE(h.group_in_user("other"));
}
TEST(DummyLogicTest, EnvironmentProxySetTrue) {
    DummyHost h;
    EXPECT_NE(h.environment_proxy_set(), nullptr);
}
TEST(DummyLogicTest, EnvironmentProxySetFalse) {
    DummyHost h;
    h.environment_file = "";
    EXPECT_FALSE(h.environment_proxy_set());
}
TEST(DummyLogicTest, DaemonDnsOkTrue) {
    DummyHost h;
    EXPECT_TRUE(h.daemon_dns_ok());
}
TEST(DummyLogicTest, DaemonDnsOkFalse) {
    DummyHost h;
    h.daemon_json_content = "{\"log-driver\":\"journald\"}";
    EXPECT_FALSE(h.daemon_dns_ok());
}
TEST(DummyLogicTest, CronCleanUpJobValidTrue) {
    DummyHost h;
    EXPECT_TRUE(h.cron_clean_up_job_valid());
}
TEST(DummyLogicTest, CronCleanUpJobValidFalse) {
    DummyHost h;
    h.cron_file = "";
    EXPECT_FALSE(h.cron_clean_up_job_valid());
}