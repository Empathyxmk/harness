#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <nlohmann/json.hpp>
#include <stdexcept>
#include <algorithm>

// DummyContainer mimics the one in the Python code
struct DummyExecRunOutPublic {
    std::string output;
};
struct DummyContainerPublic {
    nlohmann::json _top;
    DummyExecRunOutPublic _exec_run_out;
    std::string _logs_bytes;
    bool _stop_called;
    bool _remove_called;
    bool _raise_on_top;
    bool _raise_on_exec_run;
    bool _has_gunicorn;
    DummyContainerPublic(
        std::optional<nlohmann::json> top = std::nullopt,
        std::optional<DummyExecRunOutPublic> exec_run_out = std::nullopt,
        std::optional<std::string> logs_bytes = std::nullopt,
        bool has_gunicorn=true,
        bool raise_on_top=false,
        bool raise_on_exec_run=false
    ) :
      _top(top.value_or(
        has_gunicorn?
            nlohmann::json::parse("{\"Processes\": [[\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\", \"gunicorn -w 3 -b :5000 anotherapp:app\"]]}"):
            nlohmann::json::parse("{\"Processes\": [[\"z\",\"y\",\"x\",\"w\",\"v\",\"u\",\"t\",\"python manage.py\"]]}")
      )),
      _exec_run_out(exec_run_out.value_or(DummyExecRunOutPublic{"{\"bar\": 43}"})),
      _logs_bytes(logs_bytes.value_or("Different logs")),
      _stop_called(false), _remove_called(false),
      _raise_on_top(raise_on_top), _raise_on_exec_run(raise_on_exec_run),
      _has_gunicorn(has_gunicorn) {}

    nlohmann::json top() const {
        if (_raise_on_top) throw std::runtime_error("Top method failed for container");
        return _top;
    }
    DummyExecRunOutPublic exec_run(const std::string&) const {
        if (_raise_on_exec_run) throw std::runtime_error("exec_run simulated failure");
        return _exec_run_out;
    }
    std::string logs() const { return _logs_bytes; }
    void stop() { _stop_called = true; }
    void remove() { _remove_called = true; }
};

struct DummyClientPublic {
    struct Containers {
        struct NotFound: std::exception {};
        DummyContainerPublic* _container;
        bool _notfound;
        Containers(DummyContainerPublic* container=nullptr, bool notfound=false) : _container(container), _notfound(notfound) {}
        DummyContainerPublic& get(const std::string&) {
            if (_notfound) throw NotFound();
            return *_container;
        }
    } containers;
    DummyClientPublic(DummyContainerPublic* container=nullptr, bool notfound=false): containers(container, notfound) {}
};

static std::vector<std::string> get_process_names(const DummyContainerPublic& c) {
    auto t = c.top();
    std::vector<std::string> names;
    for(const auto& p: t["Processes"]) {
        if (p.is_array() && p.size() > 7) {
            std::string name = p[7];
            if (name.find("gunicorn") != std::string::npos)
                names.push_back(name);
        }
    }
    return names;
}
static std::string get_gunicorn_conf_path(const DummyContainerPublic& c) {
    auto t = c.top();
    for(const auto& p: t["Processes"]) {
        if (p.is_array() && p.size() > 7) {
            std::string name = p[7];
            if (name.find("gunicorn") != std::string::npos) {
                auto pos = name.find("-c ");
                if (pos != std::string::npos) {
                    std::string sub = name.substr(pos+3);
                    size_t space = sub.find(' ');
                    return (space != std::string::npos) ? sub.substr(0,space):sub;
                } else throw std::out_of_range("No -c conf in gunicorn process.");
            }
        }
    }
    throw std::out_of_range("No gunicorn process");
}
static std::map<std::string, int> get_config(const DummyContainerPublic& c) {
    DummyExecRunOutPublic out = c.exec_run("cat conf.json");
    auto j = nlohmann::json::parse(out.output);
    std::map<std::string, int> result;
    for(auto it=j.begin(); it!=j.end(); ++it) {
        if (it.value().is_number_integer()) result[it.key()] = it.value();
        else if (it.value().is_number()) result[it.key()] = static_cast<int>(it.value());
    }
    return result;
}
static void remove_previous_container(DummyClientPublic& cli) {
    try {
        DummyContainerPublic& c = cli.containers.get("main_container");
        c.stop();
        c.remove();
    } catch(const DummyClientPublic::Containers::NotFound&) {
        // do nothing
    }
}
static std::string get_logs(const DummyContainerPublic& c) {
    auto bytes = c.logs();
    for(char ch: bytes) {
        if ((unsigned char)ch >= 128) throw std::runtime_error("UnicodeDecodeError");
    }
    return bytes;
}
static std::string get_response_text1() {
    std::string python_version = "3.10";
    return "Hello World from Flask in a Docker container running Python " + python_version;
}

TEST(PublicUtils, GetProcessNames) {
    DummyContainerPublic c;
    auto res = get_process_names(c);
    EXPECT_FALSE(res.empty());
    EXPECT_NE(std::find(res.begin(), res.end(), "gunicorn -w 3 -b :5000 anotherapp:app"), res.end());
}
TEST(PublicUtils, GetProcessNamesEmpty) {
    DummyContainerPublic c(/*top*/std::nullopt, /*exec_run_out*/std::nullopt, /*logs*/std::nullopt, false);
    auto res = get_process_names(c);
    EXPECT_TRUE(res.empty());
}
TEST(PublicUtils, GetGunicornConfPath) {
    nlohmann::json top = nlohmann::json::parse("{\"Processes\": [[\"1\",\"2\",\"3\",\"4\",\"5\",\"6\",\"7\", \"gunicorn -c custom_conf.py anotherapp:app\"]]}");
    DummyContainerPublic c(top);
    auto path = get_gunicorn_conf_path(c);
    EXPECT_EQ(path, "custom_conf.py");
}
TEST(PublicUtils, GetGunicornConfPathNoGunicorn) {
    DummyContainerPublic c(std::nullopt,std::nullopt,std::nullopt,false);
    EXPECT_THROW({ get_gunicorn_conf_path(c); }, std::out_of_range);
}
TEST(PublicUtils, GetConfig) {
    DummyContainerPublic c(std::nullopt, DummyExecRunOutPublic{"{\"baz\":99}"});
    auto config = get_config(c);
    EXPECT_EQ(config["baz"], 99);
}
TEST(PublicUtils, GetConfigExecRunError) {
    DummyContainerPublic c(std::nullopt, std::nullopt, std::nullopt, true, false, true);
    EXPECT_THROW({ get_config(c); }, std::runtime_error);
}
TEST(PublicUtils, RemovePreviousContainerFound) {
    auto c = std::make_unique<DummyContainerPublic>();
    DummyClientPublic cli(c.get(), false);
    remove_previous_container(cli);
    EXPECT_TRUE(c->_stop_called);
    EXPECT_TRUE(c->_remove_called);
}
TEST(PublicUtils, RemovePreviousContainerNotFound) {
    DummyClientPublic cli(nullptr, true);
    EXPECT_NO_THROW({remove_previous_container(cli);});
}
TEST(PublicUtils, GetLogs) {
    DummyContainerPublic c(std::nullopt, std::nullopt, std::string("xyz789"));
    auto logs = get_logs(c);
    EXPECT_EQ(logs, "xyz789");
}
TEST(PublicUtils, GetResponseText1) {
    auto msg = get_response_text1();
    EXPECT_NE(msg.find("3.10"), std::string::npos);
}
TEST(PublicUtils, GetLogsUtf8Error) {
    struct BadContainerPublic: public DummyContainerPublic {
        BadContainerPublic() : DummyContainerPublic() {}
        std::string logs() const override { return std::string("\xfe",1); }
    };
    BadContainerPublic c;
    EXPECT_THROW({get_logs(c);}, std::runtime_error);
}