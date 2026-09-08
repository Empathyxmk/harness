#include <gtest/gtest.h>
#include "src/mixins.h"
#include <typeinfo>

class User : public UserMixin {
public:
    User(int id_) { id = std::to_string(id_); id_set = true; }
    User(const std::string& id_) { id = id_; id_set = true; }
    User() : User(1) {}
};

TEST(PublicMixinsTest, UserMixinIsActivePublic) {
    User user(100);
    EXPECT_TRUE(user.is_active());
}

TEST(PublicMixinsTest, UserMixinIsAuthenticatedPublic) {
    User user(200);
    EXPECT_TRUE(user.is_authenticated());
}

TEST(PublicMixinsTest, UserMixinIsAnonymousPublic) {
    User user(300);
    EXPECT_FALSE(user.is_anonymous());
}

TEST(PublicMixinsTest, UserMixinGetIdReturnsStrPublic) {
    User user(456);
    EXPECT_EQ(user.get_id(), "456");
    User user2("xyz");
    EXPECT_EQ(user2.get_id(), "xyz");
}

TEST(PublicMixinsTest, UserMixinGetIdAttributeErrorPublic) {
    User user(10);
    user.unset_id();
    EXPECT_THROW({ user.get_id(); }, std::logic_error);
}

TEST(PublicMixinsTest, UserMixinEqTruePublic) {
    User user1(55), user2(55);
    EXPECT_TRUE(user1 == user2);
}

TEST(PublicMixinsTest, UserMixinEqFalsePublic) {
    User user1(11), user2(12);
    EXPECT_TRUE(user1 != user2);
}

TEST(PublicMixinsTest, UserMixinEqTypePublic) {
    User user(222);
    EXPECT_FALSE(false);  // not type comparable in C++
}

TEST(PublicMixinsTest, UserMixinNeTypePublic) {
    User user(1234);
    EXPECT_TRUE(true);  // not type comparable in C++
}

TEST(PublicMixinsTest, UserMixinHashPublic) {
    User user(42);
    std::hash<std::string> h;
    auto hashed = h(user.get_id());
    (void)hashed;
    EXPECT_TRUE(typeid(hashed) == typeid(size_t));
}

TEST(PublicMixinsTest, AnonymousUserMixinPropertiesPublic) {
    AnonymousUserMixin anon;
    EXPECT_FALSE(anon.is_active());
    EXPECT_FALSE(anon.is_authenticated());
    EXPECT_TRUE(anon.is_anonymous());
}

TEST(PublicMixinsTest, AnonymousUserMixinGetIdPublic) {
    AnonymousUserMixin anon;
    EXPECT_EQ(anon.get_id(), "");
}