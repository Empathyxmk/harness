#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <tuple>
#include <map>
#include <functional>
#include <memory>

// Simulate DriverProxy and its test logic for public tests.

class AnotherDummyEngine {
public:
    std::vector<std::pair<std::string, std::map<std::string, std::string>>> notified;
    void _notify(const std::string& topic, std::map<std::string, std::string> kwargs) {
        notified.push_back({topic, kwargs});
    }
};

class AnotherDummyDriver {
public:
    void* proxy;
    std::vector<std::pair<std::string, std::string>> said;
    bool stopped = false;
    bool busyState = false;
    AnotherDummyDriver(void* p) : proxy(p) {}
    void startLoop() {}
    void endLoop() {}
    void say(const std::string& text, const std::string& name) {
        said.emplace_back(text, name);
    }
    void stop() { stopped = true; }
    void setBusy(bool value) { busyState = value; }
    void notify(const std::map<std::string, std::string>& data) {}
};

class DriverProxyPublic {
public:
    AnotherDummyDriver* _driver;
    AnotherDummyEngine* _engine;
    bool _busy;
    std::vector<std::tuple<
        std::function<std::string(std::string)>,
        std::vector<std::string>,
        std::string // name
    >> _queue;
    std::string _name;
    DriverProxyPublic(AnotherDummyEngine* eng, std::string name = "dummy", bool debug=true)
        : _driver(new AnotherDummyDriver(this)),
          _engine(eng),
          _busy(true),
          _name(name)
    {}
    ~DriverProxyPublic() {
        delete _driver;
    }
    void setBusy(bool b) { _busy = b; _driver->setBusy(b); }
    bool isBusy() const { return _busy; }
    void _push(std::function<std::string(std::string)> fn, std::vector<std::string> args, std::string name = "") {
        _queue.push_back(std::make_tuple(fn, args, name));
    }
    void notify(const std::string& topic, std::map<std::string, std::string> kw) {
        _engine->_notify(topic, kw);
    }
    void say(const std::string& text, std::string id) {
        auto fn = [this, text, id](std::string) -> std::string {
            this->_driver->say(text, id);
            return "";
        };
        _push(fn, {text}, id);
    }
    void stop() {
        _driver->stop();
    }
};

static DriverProxyPublic* base_driverproxy_for_magic(std::string test_name = "queue", std::function<AnotherDummyDriver*(void*)> drivercls = [](void* p){return new AnotherDummyDriver(p);} ) {
    auto* eng = new AnotherDummyEngine();
    auto* proxy = new DriverProxyPublic(eng, test_name, true);
    delete proxy->_driver;
    proxy->_driver = drivercls(proxy);
    return proxy;
}

TEST(PublicDriverProxy, Init) {
    AnotherDummyEngine eng;
    DriverProxyPublic p(&eng, "otherdummy", true);
    EXPECT_NE(dynamic_cast<AnotherDummyDriver*>(p._driver), nullptr);
    EXPECT_EQ(p._engine, &eng);
    EXPECT_TRUE(p._busy);
}

TEST(PublicDriverProxy, Del) {
    auto* proxy = base_driverproxy_for_magic("del", [](void* p){return new AnotherDummyDriver(p);});
    EXPECT_NO_THROW(delete proxy);
}

TEST(PublicDriverProxy, PushAndPump) {
    auto* proxy = base_driverproxy_for_magic("push", [](void* p){return new AnotherDummyDriver(p);});
    proxy->_push([](std::string s) -> std::string { return std::string(s).append("_UPPER"); }, {"fox"});
    proxy->_push([](std::string s) -> std::string { std::string t = s; std::reverse(t.begin(), t.end()); return t; }, {"bottle"});
    std::vector<std::string> collected;
    while (!proxy->_queue.empty()) {
        auto tup = proxy->_queue.front();
        proxy->_queue.erase(proxy->_queue.begin());
        auto fn = std::get<0>(tup);
        auto args = std::get<1>(tup);
        collected.push_back(fn(args[0]));
    }
    EXPECT_EQ(collected[0], "fox_UPPER");
    EXPECT_EQ(collected[1], "elttob");
    delete proxy;
}

TEST(PublicDriverProxy, Notify) {
    auto* proxy = base_driverproxy_for_magic("notify", [](void* p){return new AnotherDummyDriver(p);});
    proxy->notify("pub_new_notify", {{"key","val"}});
    auto notified = proxy->_engine->notified;
    ASSERT_FALSE(notified.empty());
    EXPECT_EQ(notified.back().first, "pub_new_notify");
    EXPECT_EQ(notified.back().second["key"], "val");
    delete proxy;
}

TEST(PublicDriverProxy, SetBusyAndIsBusy) {
    auto* proxy = base_driverproxy_for_magic("busy", [](void* p){return new AnotherDummyDriver(p);});
    proxy->setBusy(false);
    EXPECT_FALSE(proxy->isBusy());
    proxy->setBusy(true);
    EXPECT_TRUE(proxy->isBusy());
    delete proxy;
}

TEST(PublicDriverProxy, Say) {
    class SayDriver : public AnotherDummyDriver {
    public:
        std::vector<std::pair<std::string, std::string>> said_items;
        SayDriver(void* p) : AnotherDummyDriver(p) {}
        void say(const std::string& text, const std::string& name) override {
            said_items.emplace_back(text, name);
        }
    };
    auto* proxy = base_driverproxy_for_magic("say", [](void* p){return new SayDriver(p);});
    proxy->say("Hi from public!", "pTestName");
    // Since say queues, check the queue for our function and its arguments.
    bool found = false;
    for (auto& q : proxy->_queue) {
        auto args = std::get<1>(q);
        auto name = std::get<2>(q);
        if (args[0] == "Hi from public!" && name == "pTestName") found = true;
    }
    EXPECT_TRUE(found);
    delete proxy;
}

TEST(PublicDriverProxy, Stop) {
    class StopDriver : public AnotherDummyDriver {
    public:
        int times_stopped = 0;
        StopDriver(void* p) : AnotherDummyDriver(p) {}
        void stop() override { times_stopped += 1; }
    };
    auto* proxy = base_driverproxy_for_magic("stop", [](void* p){return new StopDriver(p);});
    ((StopDriver*)(proxy->_driver))->times_stopped = 0;
    proxy->stop();
    EXPECT_EQ(((StopDriver*)(proxy->_driver))->times_stopped, 1);
    delete proxy;
}