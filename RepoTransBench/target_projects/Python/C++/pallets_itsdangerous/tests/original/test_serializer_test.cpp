#include <gtest/gtest.h>
#include "serializer.h"

TEST(SerializerTest, DumpsLoads) {
    Serializer s("secret-key");
    std::map<std::string, std::string> data{{"hello", "world"}};
    std::string dumped = s.dumps(data);
    auto loaded = s.loads(dumped);
    EXPECT_EQ(loaded, data);
}

TEST(SerializerTest, LoadsBadSignature) {
    Serializer s("secret-key");
    std::string bad_token = "bad-token";
    EXPECT_THROW({
        s.loads(bad_token);
    }, BadSignature);
}

TEST(SerializerTest, LoadsPayloadVariants) {
    Serializer s("secret-key");
    std::map<std::string, std::string> data{{"foo", "bar"}};
    std::string dumped = s.dumps(data);
    auto loaded = s.loads(dumped, /*return_payload=*/false);
    EXPECT_EQ(loaded, data);
    auto loaded_payload = s.loads(dumped, /*return_payload=*/true);
    EXPECT_EQ(loaded_payload, data);
}

TEST(SerializerTest, DumpAndLoadToFile) {
    Serializer s("secret");
    std::map<std::string, int> data{{"a",1},{"b",2}};
    std::string file_path = "/tmp/token.txt";
    s.dump(data, file_path);
    auto loaded = s.load(file_path);
    EXPECT_EQ(loaded, data);
}