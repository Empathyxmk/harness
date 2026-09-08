#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <type_traits>

#include "jsonlines/jsonlines.h"

TEST(PublicTypingTest, JsonTypeIsNlohmann) {
    static_assert(std::is_same<nlohmann::json, nlohmann::json>::value, "json type should be nlohmann::json");
}