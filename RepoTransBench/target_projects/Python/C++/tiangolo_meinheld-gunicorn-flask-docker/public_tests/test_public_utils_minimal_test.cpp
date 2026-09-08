#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <nlohmann/json.hpp>
#include <thread>
#include <chrono>
#include <iostream>

using json = nlohmann::json;

// DummyContainer for minimal public
struct DummyExecRunOutMinPub {
    std::string output;
};
struct DummyContainerMinPub {
    json _top;
    DummyExecRunOutMinPub _exec_run_out;
    std::string _logs_bytes;
    bool _raise_on_top;
    bool _raise_on_exec_run;
    bool _stop_called;
    bool _remove_called;

    DummyContainerMinPub(std::string logs_bytes="publiclog", bool raise_on_top=false, bool raise_on_exec_run=false)
    : _top(json::parse("{\"Processes\": [[\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\",\"gunicorn -b :8080 -w 2 pubapp:app\"]]}")),
      _exec_run_out(DummyExecRunOutMinPub{"{\"publickey\": \"publicvalue\"}"}),
      _logs_bytes(logs_bytes),
      _raise_on_top(raise_on_top),
      _raise_on_exec_run(raise_on_exec_run),
      _stop_called(false), _remove_called(false) {}

    json top() const {
        if (_raise_on_top) throw std::runtime_error("Dummy top error");
        return _top;
    }
    DummyExecRunOutMinPub exec_run(const std::string&) const {
        if (_raise_on_exec_run) throw std::runtime_error("Dummy exec_run error");
        return _exec_run_out;
    }
    std::string logs() const { return _logs_bytes; }
    void stop() { _stop_called = true; }
    void remove() { _remove_called = true; }
};

static bool wait_for_gunicorn(DummyContainerMinPub& c, double sleep_time, double timeout) {
    double waited = 0.0;
    while (waited < timeout) {
        auto t = c.top();
        bool found = false;
        for (const auto& p: t["Processes"]) {
            if (p.is_array() && p.size() > 7 && std::string(p[7]).find("gunicorn") != std::string::npos) {
                found = true;
            }
        }
        if (found) return true;
        std::this_thread::sleep_for(std::chrono::duration<double>(sleep_time));
        waited += sleep_time;
    }
    return false;
}

static std::map<std::string,std::string> get_config_from_container(DummyContainerMinPub& c, const std::string&) {
    try {
        DummyExecRunOutMinPub out = c.exec_run("get_config");
        auto js = json::parse(out.output);
        std::map<std::string,std::string> m;
        for(auto it=js.begin(); it!=js.end(); ++it)
            m[it.key()]=it.value();
        return m;
    } catch (...) {
        return {};
    }
}

static void print_container_logs(const DummyContainerMinPub& c) {
    std::cout << "Container logs: " << c.logs() << std::endl;
}

static void cleanup_container(DummyContainerMinPub& c) {
    c.stop();
    c.remove();
}

TEST(PublicUtilsMinimal, WaitForGunicornFound) {
    DummyContainerMinPub c;
    auto result = wait_for_gunicorn(c, 0.01, 0.06);
    EXPECT_TRUE(result);
}
TEST(PublicUtilsMinimal, WaitForGunicornAbsent) {
    DummyContainerMinPub c;
    c._top = json::parse("{\"Processes\": [[\"python worker.py\"]]}");
    auto result = wait_for_gunicorn(c, 0.01, 0.03);
    EXPECT_FALSE(result);
}
TEST(PublicUtilsMinimal, GetConfigFromContainerOk) {
    DummyContainerMinPub c;
    auto r = get_config_from_container(c, "/myconf.json");
    EXPECT_TRUE(r.find("publickey")!=r.end());
}
TEST(PublicUtilsMinimal, GetConfigFromContainerExecRunFails) {
    DummyContainerMinPub c("publiclog", false, true);
    auto r = get_config_from_container(c, "/notarealpath");
    EXPECT_TRUE(r.empty());
}
TEST(PublicUtilsMinimal, PrintContainerLogsOutput) {
    DummyContainerMinPub c;
    testing::internal::CaptureStdout();
    print_container_logs(c);
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("Container logs:"), std::string::npos);
}
TEST(PublicUtilsMinimal, CleanupContainerStopsAndRemoves) {
    DummyContainerMinPub c;
    cleanup_container(c);
    EXPECT_TRUE(c._stop_called);
    EXPECT_TRUE(c._remove_called);
}