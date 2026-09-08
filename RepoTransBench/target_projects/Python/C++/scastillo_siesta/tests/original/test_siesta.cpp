#include <gtest/gtest.h>
#include "siesta.hpp"

TEST(TestSiestaAPI, FooNotSupportedPrint) {
    EXPECT_NO_THROW(foo_not_supported());
}

TEST(TestSiestaAPI, APIInitAndAttr) {
    API api("http://api.com");
    auto resource = api.get_resource("books");
    EXPECT_TRUE(resource != nullptr);
    EXPECT_TRUE(api.resources.count("/books") > 0);
    EXPECT_EQ(resource->uri, "/books");
    EXPECT_EQ(resource->api, reinterpret_cast<DummyAPI*>(&api));
    EXPECT_EQ(api.repr(), "<API http://api.com>");
    EXPECT_EQ(resource->repr().compare(0, 10, "<Resource "), 0);
}