#include <gtest/gtest.h>
#include "siesta.hpp"

TEST(TestSiestaAPIPublic, FooNotSupportedPrint) {
    EXPECT_NO_THROW(foo_not_supported());
}

TEST(TestSiestaAPIPublic, APIInitAndAttr) {
    API api("http://publicapi.org");
    auto resource = api.get_resource("users");
    EXPECT_TRUE(resource != nullptr);
    EXPECT_TRUE(api.resources.count("/users") > 0);
    EXPECT_EQ(resource->uri, "/users");
    EXPECT_EQ(resource->api, reinterpret_cast<DummyAPI*>(&api));
    EXPECT_EQ(api.repr(), "<API http://publicapi.org>");
    EXPECT_TRUE(resource->repr().find("<Resource /users") == 0);
}