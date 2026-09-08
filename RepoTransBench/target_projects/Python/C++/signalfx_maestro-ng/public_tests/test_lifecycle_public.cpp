#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>

// --- Dummy lifecycle module for public tests ---

class DummyService {
public:
    bool enabled;
    std::string state;
    std::vector<std::string> run_action_calls;

    DummyService(bool e = true) : enabled(e), state("initialized") {}

    std::string run_action(const std::string& action) {
        run_action_calls.push_back(action);
        if (action == "activate")
            state = "activated";
        else if (action == "deactivate")
            state = "deactivated";
        else
            state = "unknown_action";
        return state;
    }
};

class DummyMaestroException : public std::exception {
    std::string msg_;
public:
    DummyMaestroException(std::string msg) : msg_(std::move(msg)) {}
    const char* what() const noexcept override { return msg_.c_str(); }
};

std::string run_service(DummyService& service, const std::string& action) {
    if (!service.enabled) return "";
    try {
        return service.run_action(action);
    } catch (const std::exception& ex) {
        throw DummyMaestroException(ex.what());
    }
}

// Tests

TEST(PublicLifecycleTest, RunEnabledServiceActivation) {
    DummyService service(true);
    run_service(service, "activate");
    ASSERT_EQ(service.run_action_calls.size(), 1);
    EXPECT_EQ(service.run_action_calls[0], "activate");
    EXPECT_EQ(service.state, "activated");
}

TEST(PublicLifecycleTest, RunDisabledServiceNoAction) {
    DummyService service(false);
    run_service(service, "activate");
    EXPECT_EQ(service.run_action_calls.size(), 0);
    EXPECT_EQ(service.state, "initialized");
}

TEST(PublicLifecycleTest, RunServiceHandlesUnknownAction) {
    DummyService service(true);
    run_service(service, "suspend");
    ASSERT_EQ(service.run_action_calls.size(), 1);
    EXPECT_EQ(service.run_action_calls[0], "suspend");
    EXPECT_EQ(service.state, "unknown_action");
}

TEST(PublicLifecycleTest, RunServiceExceptionHandling) {
    class FailingService : public DummyService {
    public:
        using DummyService::DummyService;
        std::string run_action(const std::string&) override {
            throw DummyMaestroException("Simulated failure");
        }
    };
    FailingService service(true);
    EXPECT_THROW(run_service(service, "activate"), DummyMaestroException);
}