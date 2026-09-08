#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
#include <functional>
#include <memory>

// This is a mock for the purposes of unit tests, mimicking the "driver.DriverProxy" logic.
// Since there's no real pyttsx3/driver logic in C++, we fully stub all logic as per Python test expectations.

class DummyDriver {
public:
    bool destroyed;
    std::string text_spoken;
    std::vector<std::string> say_called;
    bool busy;
    DummyDriver(void*) : destroyed(false), text_spoken(), say_called(), busy(true) {}
    bool destroy() { destroyed = true; return true; }
    void say(const std::string& text) { text_spoken = text; say_called.push_back(text); }
    std::string stop() { return "stopped"; }
};

class DummyEngine {
public:
    std::vector<std::pair<std::string, std::map<std::string, int>>> notifications;
    std::vector<std::pair<std::string, std::map<std::string, std::string>>> notifications_str;
    void _notify(const std::string& topic, std::map<std::string, int> kw) {
        notifications.emplace_back(topic, kw);
    }
    void _notify_str(const std::string& topic, std::map<std::string, std::string> kw) {
        notifications_str.emplace_back(topic, kw);
    }
};

// C++ version of a driver proxy, containing only things the tests call
class StubDriverProxy {
public:
    DummyDriver* _driver;
    DummyEngine* _engine;
    bool _busy;
    std::vector<std::tuple<std::function<void(std::string)>, std::vector<std::string>, std::string>> _queue;
    std::string _name;
    StubDriverProxy(DummyEngine* eng, bool busy = true)
        : _driver(new DummyDriver(this)), _engine(eng), _busy(busy) {}
    ~StubDriverProxy() {
        _driver->destroy();
        delete _driver;
    }
    void setBusy(bool b) { _busy = b; }
    bool isBusy() const { return _busy; }
    void _push(std::function<void(std::string)> fn, std::vector<std::string> args, std::string name = "") {
        _queue.emplace_back(fn, args, name);
        // For this test, if queue is processed immediately if not busy (Python logic)
        if (!_busy && !_queue.empty()) {
            auto tup = _queue.back();
            fn(args[0]);
            _queue.pop_back();
        }
    }
    void notify(const std::string& topic, std::map<std::string, int> kw = {}) {
        std::map<std::string, int> merged = kw;
        merged["name"] = 123; // simulate name key
        _engine->_notify(topic, merged);
    }
    void notify_str(const std::string& topic, std::map<std::string, std::string> kw = {}) {
        std::map<std::string, std::string> merged = kw;
        merged["name"] = _name;
        _engine->_notify_str(topic, merged);
    }
    void say(const std::string& text, std::string id) { _driver->say(text); }
    void stop() { _driver->stop(); }
};

TEST(DriverProxyApi, Init) {
    DummyEngine eng;
    StubDriverProxy p(&eng);
    EXPECT_NE(p._driver, nullptr);
    EXPECT_EQ(p._engine, &eng);
    EXPECT_TRUE(p._busy);
    EXPECT_EQ(p._queue.size(), size_t(0));
}

TEST(DriverProxyApi, Del) {
    DummyEngine eng;
    bool called = false;
    class DummyDrv : public DummyDriver {
    public:
        bool* called_ptr;
        DummyDrv(void* proxy, bool* p) : DummyDriver(proxy), called_ptr(p) {}
        bool destroy() override { *called_ptr = true; return true; }
    };
    class LocalProxy : public StubDriverProxy {
    public:
        DummyDrv* drv;
        LocalProxy(DummyEngine* eng, bool* called) : StubDriverProxy(eng) {
            delete _driver;
            drv = new DummyDrv(this, called);
            _driver = drv;
        }
        ~LocalProxy() { drv->destroy(); delete drv; }
    };
    {
        LocalProxy p(&eng, &called);
    }
    EXPECT_TRUE(called);
}

TEST(DriverProxyApi, PushAndPump) {
    DummyEngine eng;
    StubDriverProxy proxy(&eng);
    proxy._busy = false;
    std::vector<std::string> called;
    auto meth1 = [&](std::string text) { called.push_back(text); };
    proxy._queue.clear();
    proxy._push(meth1, {"hello"}, "tid");
    EXPECT_EQ(called.size(), 1);
    EXPECT_EQ(called[0], "hello");
}

TEST(DriverProxyApi, Notify) {
    DummyEngine eng;
    StubDriverProxy p(&eng);
    p._name = "abc";
    p.notify_str("test_topic", {{"foo", "123"}});
    ASSERT_GT(eng.notifications_str.size(), size_t(0));
    EXPECT_EQ(eng.notifications_str.back().first, "test_topic");
    EXPECT_EQ(eng.notifications_str.back().second["foo"], "123");
    EXPECT_EQ(eng.notifications_str.back().second["name"], "abc");
}

TEST(DriverProxyApi, SetBusyAndIsBusy) {
    DummyEngine eng;
    StubDriverProxy p(&eng);
    p.setBusy(false);
    EXPECT_FALSE(p.isBusy());
    p.setBusy(true);
    EXPECT_TRUE(p.isBusy());
}

TEST(DriverProxyApi, Say) {
    DummyEngine eng;
    class DummyDrv : public DummyDriver {
    public:
        DummyDrv(void* proxy) : DummyDriver(proxy) {}
        void say(const std::string& text) { text_spoken = "spoken"; }
    };
    StubDriverProxy p(&eng);
    delete p._driver;
    p._driver = new DummyDrv(&p);
    p._busy = false;
    p.say("abc", "tid");
    EXPECT_EQ(static_cast<DummyDrv*>(p._driver)->text_spoken, "spoken");
}

TEST(DriverProxyApi, Stop) {
    DummyEngine eng;
    class DummyDrv : public DummyDriver {
    public:
        bool stopped = false;
        DummyDrv(void* proxy) : DummyDriver(proxy) {}
        std::string stop() { stopped = true; return "stopped"; }
    };
    StubDriverProxy p(&eng);
    delete p._driver;
    auto drv = new DummyDrv(&p);
    p._driver = drv;
    p._queue.clear(); // test stop with empty queue
    p.stop();
    EXPECT_TRUE(drv->stopped);
}