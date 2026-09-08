#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <type_traits>

class SerializationError : public std::exception {
public:
    std::string message;
    SerializationError(const std::string& msg) : message(msg) {}
    const char* what() const noexcept override { return message.c_str(); }
};

class DeserializationError : public std::exception {
public:
    std::string message;
    std::string source;
    std::string target;
    DeserializationError(const std::string& msg, const std::string& src = "", const std::string& tgt = "")
        : message(msg), source(src), target(tgt) {}
    const char* what() const noexcept override { return message.c_str(); }
};

TEST(TestPrimitive, test_dump_str) {
    std::string dumped = "some string";
    EXPECT_EQ(dumped, "some string");
}

TEST(TestPrimitive, test_dump_int) {
    int dumped = 123;
    EXPECT_EQ(dumped, 123);
}

TEST(TestPrimitive, test_dump_float) {
    double dumped = 123.456;
    EXPECT_EQ(dumped, 123.456);
}

TEST(TestPrimitive, test_dump_bool) {
    bool dumped = true;
    EXPECT_EQ(dumped, true);
}

TEST(TestPrimitive, test_dump_none) {
    void* dumped = nullptr;
    EXPECT_EQ(dumped, nullptr);
}

TEST(TestPrimitive, test_dump_and_cast) {
    EXPECT_EQ(std::stoi("42"), 42);
    EXPECT_EQ(std::stod("42"), 42.0);
    EXPECT_EQ(std::to_string(42), "42");
    EXPECT_EQ((bool)42, true);

    EXPECT_THROW({ throw SerializationError("invalid literal for int(): 'fortytwo'"); }, SerializationError);

    try {
        throw SerializationError("invalid literal for int(): 'fortytwo'");
    } catch(const SerializationError& err) {
        EXPECT_TRUE(std::string(err.what()).find("fortytwo") != std::string::npos);
    }
}

TEST(TestPrimitive, test_load_str) {
    std::string loaded = "some string";
    EXPECT_EQ(loaded, "some string");
}

TEST(TestPrimitive, test_load_int) {
    int loaded = 123;
    EXPECT_EQ(loaded, 123);
}

TEST(TestPrimitive, test_load_float) {
    double loaded = 123.456;
    EXPECT_EQ(loaded, 123.456);
}

TEST(TestPrimitive, test_load_bool) {
    bool loaded = true;
    EXPECT_EQ(loaded, true);
}

TEST(TestPrimitive, test_load_and_cast) {
    EXPECT_EQ(std::stoi("42"), 42);
    EXPECT_EQ(std::stod("42"), 42.0);
    EXPECT_EQ(std::to_string(42), "42");
    EXPECT_EQ((bool)42, true);

    EXPECT_THROW({ throw DeserializationError("invalid literal for int(): 'fortytwo'", "fortytwo", "int"); }, DeserializationError);

    try {
        throw DeserializationError("invalid literal for int(): 'fortytwo'", "fortytwo", "int");
    } catch (const DeserializationError& err) {
        EXPECT_EQ(err.source, "fortytwo");
        EXPECT_EQ(err.target, "int");
    }
}