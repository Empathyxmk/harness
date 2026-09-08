#include <gtest/gtest.h>
#include <gmock/gmock.h>
#include <string>

// Dummy FlaskRedis and AppStub for constructor logic
class AppStub {};

class DummyFlaskRedis {
public:
    MOCK_METHOD(void, init_app, (AppStub*), ());
    DummyFlaskRedis() {}
    DummyFlaskRedis(AppStub* app) {
        init_app(app);
    }
};

// The test mimics the Python test to assert init_app gets called once with the app
TEST(TestClient, test_constructor_app) {
    DummyFlaskRedis redis;
    testing::NiceMock<DummyFlaskRedis> mockRedis;
    AppStub app;
    EXPECT_CALL(mockRedis, init_app(&app)).Times(1);
    DummyFlaskRedis(&app); // Should call init_app
}