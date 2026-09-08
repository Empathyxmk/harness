#include <gtest/gtest.h>
#include "src/test_client.h"

class DummyUser : public DummyUserLike {
public:
    DummyUser(const std::string& id) : _id(id) {}
    std::string get_id() const override { return _id; }
    std::string _id;
};

TEST(PublicClientTest, FlaskLoginClientSetsUserIdPublic) {
    auto u = std::make_shared<DummyUser>("U987");
    FlaskLoginClient client(u, false);
    auto sess = client.sess;
    ASSERT_EQ((*sess)["_user_id"], "U987");
    ASSERT_EQ((*sess)["_fresh"], "0");
}

TEST(PublicClientTest, FlaskLoginClientNoUserPublic) {
    FlaskLoginClient client(nullptr);
    auto sess = client.sess;
    ASSERT_TRUE(sess->find("_user_id") == sess->end());
    ASSERT_TRUE(sess->find("_fresh") == sess->end());
}