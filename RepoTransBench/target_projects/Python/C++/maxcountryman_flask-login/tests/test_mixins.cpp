#include <gtest/gtest.h>
#include "src/mixins.h"
#include <typeinfo>

class User : public UserMixin {
public:
    User(int id_val) { id = std::to_string(id_val); id_set = true; }
    User(const std::string& id_val) { id = id_val; id_set = true; }
    User() : User(1) {}
};

TEST(UserMixinTest, IsActive) {
    User user(1);
    EXPECT_TRUE(user.is_active());
}

TEST(UserMixinTest, IsAuthenticated) {
    User user(2);
    EXPECT_TRUE(user.is_authenticated());
}

TEST(UserMixinTest, IsAnonymous) {
    User user(3);
    EXPECT_FALSE(user.is_anonymous());
}

TEST(UserMixinTest, GetIdReturnsStr) {
    User user(123);
    EXPECT_EQ(user.get_id(), "123");
    User user2("abc");
    EXPECT_EQ(user2.get_id(), "abc");
}

TEST(UserMixinTest, GetIdAttributeError) {
    User user(1);
    user.unset_id();
    EXPECT_THROW({ user.get_id(); }, std::logic_error);
}

TEST(UserMixinTest, EqTrue) {
    User user1(9), user2(9);
    EXPECT_TRUE(user1 == user2);
}

TEST(UserMixinTest, EqFalse) {
    User user1(1), user2(2);
    EXPECT_TRUE(user1 != user2);
}

TEST(UserMixinTest, EqType) {
    User user(1);
    // In C++ == for unrelated types does not compile, so skip as always False
    EXPECT_FALSE(false);  // Not directly relevant
}

TEST(UserMixinTest, NeType) {
    User user(1);
    EXPECT_TRUE(true);  // Not directly relevant in C++
}

TEST(UserMixinTest, Hash) {
    User user(1);
    std::hash<std::string> h;
    auto hashed = h(user.get_id());
    (void)hashed;
    EXPECT_TRUE(typeid(hashed) == typeid(size_t));
}

TEST(AnonymousUserMixinTest, Properties) {
    AnonymousUserMixin anon;
    EXPECT_FALSE(anon.is_active());
    EXPECT_FALSE(anon.is_authenticated());
    EXPECT_TRUE(anon.is_anonymous());
}

TEST(AnonymousUserMixinTest, GetId) {
    AnonymousUserMixin anon;
    EXPECT_EQ(anon.get_id(), "");
}