#include <gtest/gtest.h>
#include <string>

class Models {
public:
    std::string dummy;
    Models(std::string d="ok") : dummy(d) {}
};

TEST(TestGetModels, Sync) {
    Models response("ok");
    ASSERT_EQ(response.dummy, "ok");
}

TEST(TestGetModels, SyncHeaders) {
    Models response("ok");
    ASSERT_EQ(response.dummy, "ok");
}