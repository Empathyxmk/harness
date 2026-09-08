#include "gtest/gtest.h"
#include "lib/sensei.h"

TEST(TestPublicSensei, PublicSenseiClassExists) {
    // We check that the class is defined and constructible
    EXPECT_TRUE(std::is_class<Sensei>::value);
}

TEST(TestPublicSensei, PublicSenseiInstance) {
    // Make a dummy stream
    WritelnDecorator dummy_stream(nullptr);
    Sensei s(&dummy_stream);
    EXPECT_TRUE(std::is_class<decltype(s)>::value);
}