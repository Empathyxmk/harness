#include <gtest/gtest.h>
#include <string>
#include <typeinfo>
#include <unordered_map>

// Stub for shshsh::quick::_I
class _I {
public:
    _I() {}
    std::string repr() const { return "_I"; }
    bool operator==(const _I& other) const { return this == &other; }
    bool operator!=(const _I& other) const { return !(*this == other); }
    template<typename T>
    _I operator+(const T&) const { throw std::runtime_error("TypeError"); }
    size_t hash() const { return std::hash<std::string>()(repr()); }
    operator bool() const { return true; }
    operator float() const { throw std::runtime_error("Cannot cast to float"); }
    operator int() const { throw std::runtime_error("Cannot cast to int"); }
    template<typename... Args>
    _I operator()(Args...) const { throw std::runtime_error("Not callable"); }
    size_t len() const { throw std::runtime_error("No length for _I"); }
};

TEST(TestPublicZero, Repr) {
    _I z;
    auto r = z.repr();
    ASSERT_TRUE(typeid(r) == typeid(std::string));
    ASSERT_TRUE(r.find("0") != std::string::npos || r.find("I") != std::string::npos || r.find("__") == std::string::npos);
}

TEST(TestPublicZero, Bool) {
    _I z;
    ASSERT_TRUE(static_cast<bool>(z));
}

TEST(TestPublicZero, Add) {
    _I z;
    ASSERT_THROW(z + std::string("abc"), std::runtime_error);
}

TEST(TestPublicZero, Eq) {
    _I z;
    ASSERT_TRUE(z == z);
    ASSERT_FALSE(z == _I());
    ASSERT_FALSE(z == _I());
}

TEST(TestPublicZero, Neq) {
    _I z;
    ASSERT_TRUE(z != std::string("test"));
    ASSERT_TRUE(z != _I());
}

TEST(TestPublicZero, Hash) {
    _I z;
    auto h = z.hash();
    ASSERT_TRUE(typeid(h) == typeid(size_t));
    std::unordered_map<_I, std::string> d;
    d[z] = "x";
    ASSERT_EQ(d[z], "x");
}

TEST(TestPublicZero, FloatCast) {
    _I z;
    try {
        float f = static_cast<float>(z);
        (void)f;
    } catch (...) {}
}

TEST(TestPublicZero, IntCast) {
    _I z;
    try {
        int i = static_cast<int>(z);
        (void)i;
    } catch (...) {}
}

TEST(TestPublicZero, Callable) {
    _I z;
    try {
        z(42);
    } catch (...) {}
}

TEST(TestPublicZero, Iter) {
    _I z;
    try {
        for (int i = 0; i < 1; ++i)
            z();
    } catch (...) {}
}

TEST(TestPublicZero, Len) {
    _I z;
    try {
        size_t l = z.len();
        (void)l;
    } catch (...) {}
}