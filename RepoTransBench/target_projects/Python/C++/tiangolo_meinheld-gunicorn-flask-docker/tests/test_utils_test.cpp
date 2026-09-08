#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <stdexcept>
#include <memory>
#include <optional>

// Simulate JSON parsing
#include <nlohmann/json.hpp>
using json = nlohmann::json;

namespace utils {
    // Helper functions that mimic pythonic interface for testing purposes
    std::vector<std::string> get_process_names(const struct DummyContainer&);
    std::string get_gunicorn_conf_path(const struct DummyContainer&);
    std::map<std::string, int> get_config(const struct DummyContainer&);
    void remove_previous_container(struct DummyClient&);
    std::string get_logs(const struct DummyContainer&);
    std::string get_response_text1();
}

// Minimal substitute for ENV testing
static std::map<std::string, std::string> ENV_MOCK;
static void setenv_mock(const std::string& key, const std::string& val) { ENV_MOCK[key]=val; }
static std::string getenv_mock(const std::string& key) {
    auto it = ENV_MOCK.find(key);
    if (it != ENV_MOCK.end()) return it->second;
    const char* env = getenv(key.c_str());
    return env ? std::string(env) : "";
}

// -------------------------------------------------------
// DummyContainer

struct DummyExecRunOut {
    std::string output;
};

struct DummyContainer {
    // Simulates the state held in Python object
    json _top;
    DummyExecRunOut _exec_run_out;
    std::string _logs_bytes;
    bool _stop_called;
    bool _remove_called;
    bool _raise_on_top;
    bool _raise_on_exec_run;
    bool _has_gunicorn;

    DummyContainer(
        std::optional<json> top = std::nullopt,
        std::optional<DummyExecRunOut> exec_run_out = std::nullopt,
        std::optional<std::string> logs_bytes = std::nullopt,
        bool has_gunicorn = true,
        bool raise_on_top = false,
        bool raise_on_exec_run = false
    ) :
        _top(top.value_or(
            has_gunicorn ?
                json::parse("{\"Processes\": [[\"a\",\"b\",\"c\",\"d\",\"e\",\"f\",\"g\",\"gunicorn -c conf.py app:app\"]]}") :
                json::parse("{\"Processes\": [[\"a\",\"b\",\"c\",\"d\",\"e\",\"f\",\"g\",\"python app.py\"]]}")
            )),
        _exec_run_out(exec_run_out.value_or(DummyExecRunOut{"{\"key\": \"value\"}"})),
        _logs_bytes(logs_bytes.value_or("Some logs")),
        _stop_called(false),
        _remove_called(false),
        _raise_on_top(raise_on_top),
        _raise_on_exec_run(raise_on_exec_run),
        _has_gunicorn(has_gunicorn)
    {}

    json top() const {
        if (_raise_on_top) throw std::runtime_error("Cannot get top of container");
        return _top;
    }
    DummyExecRunOut exec_run(const std::string& /*cmd*/) const {
        if (_raise_on_exec_run) throw std::runtime_error("exec_run failed");
        return _exec_run_out;
    }
    std::string logs() const { return _logs_bytes; }
    void stop() { _stop_called = true; }
    void remove() { _remove_called = true; }
};

// DummyClient
struct DummyClient {
    struct Containers {
        struct NotFound : public std::exception {};
        DummyContainer* _container;
        bool _notfound;
        Containers(DummyContainer* container=nullptr, bool notfound=false) : _container(container), _notfound(notfound) {}
        DummyContainer& get(const std::string&) {
            if (_notfound) throw NotFound();
            return *_container;
        }
    };
    Containers containers;
    DummyClient(DummyContainer* container=nullptr, bool notfound = false) : containers(container, notfound) {}
};

// --- utils function implementations for testing ---

std::vector<std::string> utils::get_process_names(const DummyContainer& c) {
    auto t = c.top();
    std::vector<std::string> names;
    for(const auto& p: t["Processes"]) {
        if (p.is_array() && p.size() > 7) {
            std::string name = p[7];
            if (name.find("gunicorn") != std::string::npos) names.push_back(name);
        }
    }
    return names;
}

std::string utils::get_gunicorn_conf_path(const DummyContainer& c) {
    auto t = c.top();
    for(const auto& p: t["Processes"]) {
        if (p.is_array() && p.size() > 7) {
            std::string name = p[7];
            if (name.find("gunicorn") != std::string::npos) {
                // Find "-c conf.py"
                auto pos = name.find("-c ");
                if(pos != std::string::npos) {
                    std::string sub = name.substr(pos+3);
                    size_t space = sub.find(' ');
                    return (space != std::string::npos) ? sub.substr(0, space) : sub;
                }
                throw std::out_of_range("No -c conf in gunicorn process.");
            }
        }
    }
    throw std::out_of_range("No gunicorn process");
}

std::map<std::string, int> utils::get_config(const DummyContainer& c) {
    DummyExecRunOut out = c.exec_run("cat conf.json");
    // Only parse {"foo":number} or similar map (for these tests)
    auto j = json::parse(out.output);
    std::map<std::string, int> result;
    for (auto it=j.begin(); it!=j.end(); ++it) {
        if (it.value().is_number_integer()) result[it.key()] = it.value();
        else if (it.value().is_number()) result[it.key()] = static_cast<int>(it.value());
    }
    return result;
}

void utils::remove_previous_container(DummyClient& cli) {
    try {
        auto& c = cli.containers.get("main_container");
        c.stop();
        c.remove();
    } catch (const DummyClient::Containers::NotFound&) {
        // do nothing, as expected
    }
}
std::string utils::get_logs(const DummyContainer& c) {
    // Simulate utf-8 decode with exception for tests
    auto bytes = c.logs();
    for(char ch: bytes) {
        // Simulate error on non-ascii/utf-8 bytes
        if ((unsigned char)ch >= 128) throw std::runtime_error("UnicodeDecodeError");
    }
    return bytes;
}

std::string utils::get_response_text1() {
    std::string python_version = getenv_mock("PYTHON_VERSION");
    if (python_version.empty()) python_version = "3.11";
    return std::string("Hello World from Flask in a Docker container running Python ") + python_version;
}

// -------------------------------------------------------
// TESTS

TEST(UtilsTest, GetProcessNames) {
    DummyContainer c;
    auto res = utils::get_process_names(c);
    EXPECT_FALSE(res.empty());
    EXPECT_NE(std::find(res.begin(), res.end(), "gunicorn -c conf.py app:app"), res.end());
}

TEST(UtilsTest, GetProcessNamesEmpty) {
    DummyContainer c(
        /*top*/std::nullopt, /*exec_run_out*/std::nullopt, /*logs_bytes*/std::nullopt,
        /*has_gunicorn*/false);
    auto res = utils::get_process_names(c);
    EXPECT_TRUE(res.empty());
}

TEST(UtilsTest, GetGunicornConfPath) {
    DummyContainer c;
    auto path = utils::get_gunicorn_conf_path(c);
    EXPECT_EQ(path, "conf.py");
}

TEST(UtilsTest, GetGunicornConfPathNoGunicorn) {
    DummyContainer c(
        /*top*/std::nullopt, /*exec_run_out*/std::nullopt, /*logs_bytes*/std::nullopt,
        /*has_gunicorn*/false);
    EXPECT_THROW({ utils::get_gunicorn_conf_path(c); }, std::out_of_range);
}

TEST(UtilsTest, GetConfig) {
    DummyContainer c(
        std::nullopt, DummyExecRunOut{"{\"foo\":42}"});
    auto config = utils::get_config(c);
    EXPECT_EQ(config["foo"], 42);
}

TEST(UtilsTest, GetConfigExecRunError) {
    DummyContainer c(
        std::nullopt, std::nullopt, std::nullopt, true, false, true // raise_on_exec_run=true
    );
    EXPECT_THROW({ utils::get_config(c); }, std::runtime_error);
}

TEST(UtilsTest, RemovePreviousContainerFound) {
    auto c = std::make_unique<DummyContainer>();
    DummyClient cli(c.get(), false);
    utils::remove_previous_container(cli);
    EXPECT_TRUE(c->_stop_called);
    EXPECT_TRUE(c->_remove_called);
}

TEST(UtilsTest, RemovePreviousContainerNotFound) {
    DummyClient cli(nullptr, true);
    // Should not throw
    EXPECT_NO_THROW({ utils::remove_previous_container(cli); });
}

TEST(UtilsTest, GetLogs) {
    DummyContainer c(
        std::nullopt, std::nullopt, std::string("abc123"));
    auto logs = utils::get_logs(c);
    EXPECT_EQ(logs, "abc123");
}

TEST(UtilsTest, GetResponseText1) {
    setenv_mock("PYTHON_VERSION", "3.9");
    auto msg = utils::get_response_text1();
    EXPECT_NE(msg.find("3.9"), std::string::npos);
}

TEST(UtilsTest, GetLogsUtf8Error) {
    struct BadContainer: public DummyContainer {
        BadContainer() : DummyContainer() {}
        std::string logs() const override { return std::string("\xff",1); }
    };
    BadContainer c;
    EXPECT_THROW({ utils::get_logs(c); }, std::runtime_error);
}