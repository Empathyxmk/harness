#include <gtest/gtest.h>
#include "graphios.h"

TEST(PublicGraphios, CreateMetricLine) {
    std::string line = create_metric_line("disk_usage", "server3", "DiskIO", "write", 0.99, 456, 678, "2024-02-10 08:00:00");
    EXPECT_EQ(line, "disk_usage,server3,DiskIO,write,0.99,456,678,2024-02-10 08:00:00");
}

TEST(PublicGraphios, ParseValue) {
    EXPECT_EQ(parse_value("52.34"), 52.34);
    EXPECT_EQ(parse_value("off"), -1.0);
}

TEST(PublicGraphios, FormatPerfdata) {
    PerfData pd;
    pd.label = "free_mem"; pd.value = 1234; pd.uom = "MB";
    pd.warn = 0; pd.crit = 0; pd.min = 128; pd.max = 4096;
    std::string result = format_perfdata(pd);
    EXPECT_TRUE(result.rfind("'free_mem'=1234MB;;;128;4096", 0) == 0);
}

TEST(PublicGraphios, SplitPerfdata) {
    std::string perfdata = "'cpu'=15%;20;30;0;100 'mem'=4096MB;;;128;16384";
    auto pd_list = split_perfdata(perfdata);
    if (pd_list.size() > 0) {
        EXPECT_EQ(pd_list.back().label, "mem");
        EXPECT_EQ(pd_list.back().value, 4096);
        EXPECT_EQ(pd_list.back().uom, "MB");
    }
}

TEST(PublicGraphios, StripPerfLabel) {
    EXPECT_EQ(strip_perf_label("'swap'"), "swap");
    EXPECT_EQ(strip_perf_label("disk"), "disk");
}

TEST(PublicGraphios, IsNumeric) {
    EXPECT_TRUE(is_numeric("483.3"));
    EXPECT_FALSE(is_numeric("test998"));
}

TEST(PublicGraphios, Perfdata2List) {
    std::string pd = "'io_read'=1MB 'io_write'=2MB;;;0;100";
    auto res = perfdata2list(pd);
    EXPECT_EQ(res[0].label, "io_read");
    EXPECT_EQ(res[1].label, "io_write");
}