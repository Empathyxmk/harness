#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <type_traits>

// These "typing" tests are meta-level checks: in Python, they'd check static typing with mypy.
// In C++, we check that exported types are as expected using type_traits.

#include "jsonlines/jsonlines.h"

TEST(JsonLinesTypingTest, TypesAreCorrectlyDefined) {
    using json = nlohmann::json;
    // The value_type of the JsonLinesReader iterator should be nlohmann::json
    static_assert(std::is_same<json, nlohmann::json>::value, "json type alias should be nlohmann::json");
}

// You could add further type/interface checks if there are other public types.