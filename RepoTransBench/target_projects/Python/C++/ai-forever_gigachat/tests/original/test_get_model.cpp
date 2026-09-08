#include <gtest/gtest.h>
#include <string>

class Model {
public:
    std::string id;
    Model(std::string i) : id(i) {}
};

TEST(TestGetModel, Sync) {
    Model response("MODEL1");
    ASSERT_EQ(response.id, "MODEL1");
}

TEST(TestGetModel, SyncHeaders) {
    Model response("MODEL1");
    ASSERT_EQ(response.id, "MODEL1");
}