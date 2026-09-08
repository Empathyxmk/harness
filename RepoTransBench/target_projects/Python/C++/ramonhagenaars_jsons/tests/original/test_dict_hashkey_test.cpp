#include <gtest/gtest.h>
#include <map>
#include <string>
#include <tuple>

// Simulate a NamedTuple like type
struct Foo {
    int a, b, c;
    Foo(int x, int y, int z) : a(x), b(y), c(z) {}
    bool operator==(const Foo& other) const { return a == other.a && b == other.b && c == other.c; }
    bool operator<(const Foo& other) const {
        return std::tie(a, b, c) < std::tie(other.a, other.b, other.c);
    }
};

struct D {
    int a, b;
    D(int x, int y) : a(x), b(y) {}
    bool operator==(const D& other) const { return a == other.a && b == other.b; }
};

std::string foo_serializer(const Foo& obj) {
    return std::to_string(obj.a) + "," + std::to_string(obj.b) + "," + std::to_string(obj.c);
}
Foo foo_deserializer(const std::string& str) {
    int a, b, c;
    sscanf(str.c_str(), "%d,%d,%d", &a, &b, &c);
    return Foo(a, b, c);
}

using FooDMap = std::map<std::string, D>;

TEST(TestDictHashKey, test_dict_hashkey_with_serializer) {
    Foo foo(1,2,3);
    D d(42,39);
    FooDMap bar = { { foo_serializer(foo), d } };
    FooDMap dumped = bar;
    FooDMap expected = { {"1,2,3", D(42,39)} };
    EXPECT_EQ(dumped, expected);

    // Simulate load back
    FooDMap loaded = dumped;
    EXPECT_EQ(loaded, bar);
}

TEST(TestDictHashKey, test_dict_hashkey) {
    Foo foo(1,2,3);
    D d(42,39);
    FooDMap bar = { { foo_serializer(foo), d } };
    FooDMap dumped = bar;
    FooDMap loaded = dumped;
    EXPECT_EQ(loaded, bar);
}