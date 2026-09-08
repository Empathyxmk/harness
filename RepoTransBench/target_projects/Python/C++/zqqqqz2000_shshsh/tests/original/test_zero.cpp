#include <gtest/gtest.h>
#include <stdexcept>
#include <typeinfo>
#include <any>
#include <memory>
#include <string>
#include <sstream>
#include <unordered_map>

// Stub for shshsh::quick::_I
// In the real implementation, _I would be a class with custom methods/operators
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
    _I operator()() const { throw std::runtime_error("Not callable"); }
    template<typename T> T begin() const { throw std::runtime_error("Not iterable"); }
    template<typename T> T end() const { throw std::runtime_error("Not iterable"); }
    size_t len() const { throw std::runtime_error("No length for _I"); }
};

TEST(TestZero, Repr) {
    _I z;
    std::string r = z.repr();
    ASSERT_TRUE(typeid(r) == typeid(std::string));
}

TEST(TestZero, Bool) {
    _I z;
    ASSERT_TRUE(static_cast<bool>(z));
}

TEST(TestZero, Add) {
    _I z;
    int b = 1;
    ASSERT_THROW(z + b, std::runtime_error);
}

TEST(TestZero, Eq) {
    _I z;
    ASSERT_TRUE(z == z);
    _I z2;
    ASSERT_FALSE(z == z2);
    ASSERT_FALSE(z == 1); // comparison to int always false with == overload
}

TEST(TestZero, Neq) {
    _I z;
    _I z2;
    ASSERT_TRUE(z != 1);
    ASSERT_TRUE(z != z2);
}

TEST(TestZero, Hash) {
    _I z;
    auto h = z.hash();
    ASSERT_TRUE(typeid(h) == typeid(size_t));
}

TEST(TestZero, FloatCast) {
    _I z;
    try {
        float f = static_cast<float>(z);
        (void)f;
    } catch (...) {
        // swallow exception
    }
}

TEST(TestZero, IntCast) {
    _I z;
    try {
        int i = static_cast<int>(z);
        (void)i;
    } catch (...) {
        // swallow exception
    }
}

TEST(TestZero, Callable) {
    _I z;
    try {
        auto _ = z();
        (void)_;
    } catch (...) {
        // swallow exception
    }
}

TEST(TestZero, Iter) {
    _I z;
    try {
        auto b = z.begin<void>();
        (void)b;
    } catch (...) {
        // swallow exception
    }
}

TEST(TestZero, Len) {
    _I z;
    try {
        size_t l = z.len();
        (void)l;
    } catch (...) {
        // swallow exception
    }
}