#include <gtest/gtest.h>
#include <string>
#include <map>
#include <vector>
#include <nlohmann/json.hpp>
#include <thread>
#include <chrono>
#include <iostream>

using json = nlohmann::json;

// Minimal DummyContainer for minimal util tests
struct DummyExecRunOutMin {
    std::string output;
};
struct DummyContainerMin {
    json _top;
    DummyExecRunOutMin _exec_run_out;
    std::string _logs_bytes;
    bool _raise_on_top;
    bool _raise_on_exec_run;
    bool _stop_called;
    bool _remove_called;

    DummyContainerMin(std::string logs_bytes="logdata", bool raise_on_top=false, bool raise_on_exec_run=false)
    : _top(json::parse("{\"Processes\": [[\"a\",\"b\",\"c\",\"d\",\"e\",\"f\",\"g\",\"gunicorn -c conf.py app:app\"]]}")),
      _exec_run_out(DummyExecRunOutMin{"{\"newkey\": \"newvalue\"}"}),
      _logs_bytes(logs_bytes),
      _raise_on_top(raise_on_top),
      _raise_on_exec_run(raise_on_exec_run),
      _stop_called(false), _remove_called(false) {}

    json top() const {
        if (_raise_on_top) throw std::runtime_error("Simulate top error");
        return _top;
    }
    DummyExecRunOutMin exec_run(const std::string&) const {
        if (_raise_on_exec_run) throw std::runtime_error("Simulate exec_run error");
        return _exec_run_out;
    }
    std::string logs() const { return _logs_bytes; }
    void stop() { _stop_called = true; }
    void remove() { _remove_called = true; }
};

bool wait_for_gunicorn(DummyContainerMin& c, double sleep_time, double timeout) {
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

std::map<std::string,std::string> get_config_from_container(DummyContainerMin& c, const std::string&) {
    try {
        DummyExecRunOutMin out = c.exec_run("get_config");
        auto js = nlohmann::json::parse(out.output);
        std::map<std::string,std::string> m;
        for(auto it=js.begin(); it!=js.end(); ++it)
            m[it.key()]=it.value();
        return m;
    } catch (...) {
        return {};
    }
}

void print_container_logs(const DummyContainerMin& c) {
    std::cout << "Container logs: " << c.logs() << std::endl;
}

void cleanup_container(DummyContainerMin& c) {
    c.stop();
    c.remove();
}

TEST(UtilsMinimal, WaitForGunicornFound) {
    DummyContainerMin c;
    auto result = wait_for_gunicorn(c, 0.01, 0.05);
    EXPECT_TRUE(result);
}
TEST(UtilsMinimal, WaitForGunicornNotFound) {
    DummyContainerMin c;
    c._top = json::parse("{\"Processes\": [[\"python app.py\"]]}");
    auto result = wait_for_gunicorn(c, 0.01, 0.03);
    EXPECT_FALSE(result);
}
TEST(UtilsMinimal, GetConfigFromContainerSuccess) {
    DummyContainerMin c;
    auto r = get_config_from_container(c, "/etc/config.json");
    EXPECT_TRUE(r.find("newkey")!=r.end());
}
TEST(UtilsMinimal, GetConfigFromContainerExecRunFail) {
    DummyContainerMin c("logdata", false, true); // raise_on_exec_run=true
    auto r = get_config_from_container(c, "/fakepath");
    EXPECT_TRUE(r.empty());
}
TEST(UtilsMinimal, PrintContainerLogsPrints) {
    DummyContainerMin c;
    testing::internal::CaptureStdout();
    print_container_logs(c);
    std::string output = testing::internal::GetCapturedStdout();
    EXPECT_NE(output.find("Container logs:"), std::string::npos);
}
TEST(UtilsMinimal, CleanupContainerCallsMethods) {
    DummyContainerMin c;
    cleanup_container(c);
    EXPECT_TRUE(c._stop_called);
    EXPECT_TRUE(c._remove_called);
}