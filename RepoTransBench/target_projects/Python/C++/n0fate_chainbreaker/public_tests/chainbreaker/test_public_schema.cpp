#include <gtest/gtest.h>
#include <typeinfo>
#include <string>

namespace chainbreaker_schema {
    const char *__file__ = "schema.cpp";
    const char *__doc__ = "Doc of schema";
}

TEST(PublicSchemaTest, PublicSchemaAttributes) {
    ASSERT_TRUE(chainbreaker_schema::__file__ != nullptr || chainbreaker_schema::__doc__ != nullptr);
}

TEST(PublicSchemaTest, PublicSchemaTypeOfModule) {
    // In C++ we'd be using type_info
    ASSERT_TRUE(typeid(chainbreaker_schema::__doc__).name() != nullptr);
}