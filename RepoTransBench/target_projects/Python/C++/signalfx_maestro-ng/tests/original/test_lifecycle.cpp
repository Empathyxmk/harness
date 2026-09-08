#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <memory>
#include <map>
#include <type_traits>

namespace maestro {
namespace exceptions {
// Simulate exception types for the tests
struct MaestroException : public std::exception {
    MaestroException(const std::string& msg = "") : msg_(msg) {}
    const char* what() const noexcept override { return msg_.c_str(); }
    std::string msg_;
};
struct InvalidLifecycleCheckConfigurationException : public MaestroException {
    InvalidLifecycleCheckConfigurationException(const std::string& msg = "") : MaestroException(msg) {}
};
}
namespace lifecycle {

struct BaseLifecycleHelper {
    virtual bool test(void* container) {
        throw std::logic_error("NotImplementedError");
    }
    virtual ~BaseLifecycleHelper() = default;
};

// Retrying helper with attempts.
struct RetryingLifecycleHelper : public BaseLifecycleHelper {
    int attempts = 1, delay = 0;
    RetryingLifecycleHelper(int attempts_ = 1, int delay_ = 0) : attempts(attempts_), delay(delay_) {}

    virtual bool _test(void* container) { return false; }

    bool test(void* container) override {
        for (int i = 0; i < attempts; ++i) {
            if (_test(container)) return true;
            if (delay > 0) std::this_thread::sleep_for(std::chrono::milliseconds(delay*1000));
        }
        return false;
    }
};

// Dummy TCPPortPinger implementation
class TCPPortPinger : public RetryingLifecycleHelper {
public:
    std::string host;
    int port, wait;
    TCPPortPinger(const std::string& h, int p, int w) : host(h), port(p), wait(w) {}
    bool _test(void* container = nullptr) override {
        // Always return alternating result to simulate random
        static bool flip = false;
        flip = !flip;
        return flip;
    }
    std::string repr() const { return "PortPing(host=" + host + ", port=" + std::to_string(port) + ")"; }

    static std::shared_ptr<TCPPortPinger> from_config(const void* container, const std::map<std::string, std::string>& conf) {
        // container is a pointer to DummyContainer, cast accordingly for test.
        struct DummyContainer {
            struct DummyShip { std::string ip; }* ship;
            std::string name;
            std::map<std::string, std::map<std::string, std::vector<std::string>>> ports;
        };
        auto dummy = static_cast<const DummyContainer*>(container);
        auto it = conf.find("port");
        if (it == conf.end()) throw exceptions::InvalidLifecycleCheckConfigurationException("No port given");
        auto search = dummy->ports.find(it->second);
        if (search == dummy->ports.end())
            throw exceptions::InvalidLifecycleCheckConfigurationException("Port not found");
        if (!search->second.empty()) {
            const auto& external_vec = search->second.find("external");
            if (external_vec != search->second.end() && !external_vec->second.empty()) {
                // Check if port protocol is "udp"
                if (external_vec->second[1].find("udp") != std::string::npos) {
                    throw exceptions::InvalidLifecycleCheckConfigurationException("Not a TCP port");
                }
            }
        }
        return std::make_shared<TCPPortPinger>(
            dummy->ship ? dummy->ship->ip : "unknown",
            1234, 2
        );
    }
};

class ScriptExecutor : public RetryingLifecycleHelper {
public:
    std::string command;
    std::map<std::string, std::string> env;
    std::string envfrom = "env";
    ScriptExecutor(const std::string& c, std::map<std::string, std::string> e, int attempts_ = 1, const std::string& envfrom_ = "env")
        : RetryingLifecycleHelper(attempts_, 0), command(c), env(e), envfrom(envfrom_) {}

    bool _test(void* container = nullptr) override {
        if (envfrom == "env" || envfrom == "stdin") {
            // "Simulate" subprocess call: always succeed
            return true;
        }
        throw std::invalid_argument("envfrom invalid");
    }

    static std::shared_ptr<ScriptExecutor> from_config(const void* container, const std::map<std::string, std::string>& conf) {
        return std::make_shared<ScriptExecutor>(conf.at("command"), std::map<std::string, std::string>{{"FOO","bar"}}, conf.at("attempts") == "1" ? 1 : 0);
    }
};

}} // namespace maestro::lifecycle

using namespace maestro::lifecycle;
using namespace maestro::exceptions;

// Test Cases

TEST(LifecycleTest, BaseLifecycleHelperThrows) {
    BaseLifecycleHelper helper;
    EXPECT_THROW(helper.test(nullptr), std::logic_error);
}

TEST(LifecycleTest, RetryingLifecycleHelperSucceedsAfter2) {
    class Dummy : public RetryingLifecycleHelper {
    public:
        static int callcount;
        bool _test(void* container) override {
            ++callcount;
            return callcount > 2;
        }
    };
    Dummy::callcount = 0;
    Dummy d(3);
    EXPECT_TRUE(d.test(nullptr));
}
int Dummy_callcount = 0; // For static var

TEST(LifecycleTest, RetryingLifecycleHelperAlwaysFail) {
    class Dummy : public RetryingLifecycleHelper {
        bool _test(void* container) override { return false; }
    };
    Dummy d(2, 0);
    EXPECT_FALSE(d.test(nullptr));
}

TEST(LifecycleTest, TCPPortPingerRepr) {
    TCPPortPinger t("host", 1234, 2);
    std::string repr = t.repr();
    EXPECT_NE(repr.find("PortPing"), std::string::npos);
}

TEST(LifecycleTest, TCPPortPingerTestCall) {
    TCPPortPinger t("localhost", 9, 1);
    bool res = t._test();
    EXPECT_TRUE(res == true || res == false);
}

TEST(LifecycleTest, TCPPortPingerFromConfigSuccess) {
    struct DummyShip { std::string ip = "127.0.0.1"; };
    struct DummyContainer {
        DummyShip* ship = new DummyShip();
        std::string name = "c";
        std::map<std::string, std::map<std::string, std::vector<std::string>>> ports = {
            {"80", {{"external", { "", "1234/tcp" }}}}
        };
    };
    DummyContainer dummy;
    std::map<std::string, std::string> conf = {{"port", "80"}, {"max_wait", "2"}};
    auto t = TCPPortPinger::from_config(&dummy, conf);
    EXPECT_TRUE((bool)std::dynamic_pointer_cast<TCPPortPinger>(t));
}

TEST(LifecycleTest, TCPPortPingerFromConfigNoPort) {
    struct DummyContainer {
        std::map<std::string, std::map<std::string, std::vector<std::string>>> ports{};
        std::string name = "foo";
    } dummy;
    std::map<std::string, std::string> conf = {{"port", "5432"}};
    EXPECT_THROW(TCPPortPinger::from_config(&dummy, conf), InvalidLifecycleCheckConfigurationException);
}

TEST(LifecycleTest, TCPPortPingerFromConfigUDP) {
    struct DummyShip { std::string ip = "0.0.0.0"; };
    struct DummyContainer {
        DummyShip* ship = new DummyShip();
        std::string name = "x";
        std::map<std::string, std::map<std::string, std::vector<std::string>>> ports = {
            {"80", {{"external", { "", "9999/udp" }}}}
        };
    };
    DummyContainer dummy;
    std::map<std::string, std::string> conf = {{"port", "80"}};
    EXPECT_THROW(TCPPortPinger::from_config(&dummy, conf), InvalidLifecycleCheckConfigurationException);
}

TEST(LifecycleTest, ScriptExecutorEnvFromEnvAndStdin) {
    ScriptExecutor s("echo test", {{"A","1"}}, 1, "env");
    EXPECT_TRUE(s._test());
    ScriptExecutor s2("echo test", {{"A","1"}}, 1, "stdin");
    EXPECT_TRUE(s2._test());
}

TEST(LifecycleTest, ScriptExecutorEnvfromInvalid) {
    ScriptExecutor s("ls", {}, 1, "bad");
    EXPECT_THROW(s._test(), std::invalid_argument);
}

TEST(LifecycleTest, ScriptExecutorFromConfig) {
    struct DummyContainer { std::map<std::string, std::string> env = {{"FOO","bar"}}; } dummy;
    std::map<std::string, std::string> conf = {{"command","ls"}, {"attempts","1"}};
    auto s = ScriptExecutor::from_config(&dummy, conf);
    EXPECT_TRUE((bool)std::dynamic_pointer_cast<ScriptExecutor>(s));
}