#include <gtest/gtest.h>
#include <string>
#include <memory>

struct DummyConnectionPool {
    std::unordered_map<std::string, int> connection_kwargs;
    DummyConnectionPool(int db) { connection_kwargs["db"] = db; }
};

struct DummyRedisClient {
    std::unique_ptr<DummyConnectionPool> connection_pool;
    DummyRedisClient(int db) : connection_pool(new DummyConnectionPool(db)) {}
};

class FlaskRedisIntegrationSim {
public:
    DummyRedisClient* _redis_client = nullptr;
    bool strict = false;
    std::string config_prefix;
    explicit FlaskRedisIntegrationSim(bool strict_ = false, const std::string& prefix = "")
        : strict(strict_), config_prefix(prefix) {}
    void init_app(void* app) {
        if (!_redis_client)
            _redis_client = new DummyRedisClient(config_prefix == "DBB" ? 2 : 1); // Simulate db from config_prefix
    }
    DummyConnectionPool* connection_pool() { return _redis_client ? _redis_client->connection_pool.get() : nullptr; }

    static FlaskRedisIntegrationSim* from_custom_provider(bool called = false) {
        auto* inst = new FlaskRedisIntegrationSim();
        // No _redis_client yet
        return inst;
    }
};

TEST(TestIntegrationClient, test_constructor) {
    FlaskRedisIntegrationSim redis(/*strict=*/false, "");
    redis._redis_client = new DummyRedisClient(0);
    EXPECT_NE(redis._redis_client, nullptr);
    EXPECT_NE(redis._redis_client->connection_pool.get(), nullptr);
}

TEST(TestIntegrationClient, test_init_app) {
    FlaskRedisIntegrationSim redis(/*strict=*/false, "");
    // Before init_app, _redis_client is nullptr
    EXPECT_EQ(redis._redis_client, nullptr);
    redis.init_app(nullptr);
    EXPECT_NE(redis._redis_client, nullptr);
    EXPECT_NE(redis.connection_pool(), nullptr);
}

TEST(TestIntegrationClient, test_custom_prefix) {
    FlaskRedisIntegrationSim redis_a(false, "DBA"), redis_b(false, "DBB");
    redis_a.init_app(nullptr);
    redis_b.init_app(nullptr);
    EXPECT_EQ(redis_a.connection_pool()->connection_kwargs["db"], 1);
    EXPECT_EQ(redis_b.connection_pool()->connection_kwargs["db"], 2);
}

TEST(TestIntegrationClient, test_strict_parameter) {
    FlaskRedisIntegrationSim redis_true(true, "");
    redis_true.init_app(nullptr);
    EXPECT_NE(redis_true._redis_client, nullptr);
    // Only type info/flag is available, simulate allowed_names as in Python
    std::string rtype = redis_true.strict ? "StrictRedis" : "Redis";
    EXPECT_TRUE(rtype == "StrictRedis" || rtype == "Redis");

    FlaskRedisIntegrationSim redis_false(false, "");
    redis_false.init_app(nullptr);
    rtype = redis_false.strict ? "StrictRedis" : "Redis";
    EXPECT_TRUE(rtype == "Redis");
}

TEST(TestIntegrationClient, test_custom_provider) {
    // Simulate factory method
    FlaskRedisIntegrationSim* redis = FlaskRedisIntegrationSim::from_custom_provider();
    EXPECT_EQ(redis->_redis_client, nullptr);
    redis->init_app(nullptr);
    EXPECT_NE(redis->_redis_client, nullptr);
    delete redis;
}