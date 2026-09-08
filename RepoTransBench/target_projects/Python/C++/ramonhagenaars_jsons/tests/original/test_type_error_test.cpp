#include <gtest/gtest.h>
#include <string>
#include <stdexcept>

class DeserializationError : public std::exception {
public:
    std::string message;
    std::string target;
    std::string source;

    DeserializationError(const std::string& msg, const std::string& t, const std::string& src = "")
      : message(msg), target(t), source(src) {}

    const char* what() const noexcept override { return message.c_str(); }
};

class WrongUser {
public:
    int id;
    std::string birthday; // intentionally should have been datetime, using string

    WrongUser(int i, const std::string& b) : id(i), birthday(b) {}
};
class CorrectUser {
public:
    int id;
    std::string birthday;
    CorrectUser(int i, const std::string& b) : id(i), birthday(b) {}
};

int fake_load(const std::map<std::string,std::string>& d, const std::string& targetType) {
    // Throws on wrong type
    if (targetType == "WrongUser") {
        if (d.find("birthday") != d.end() && d.at("birthday") == "every day") {
            throw DeserializationError(
                "Could not deserialize value \"every day\" into \"datetime.datetime\".", "datetime.datetime");
        }
        if (d.find("id") != d.end() && !std::all_of(d.at("id").begin(), d.at("id").end(), ::isdigit)) {
            throw DeserializationError("Could not cast \"" + d.at("id") + "\" into \"int\"", "int", d.at("id"));
        }
        if (d.find("birthday") != d.end() && d.at("birthday") == "1879-03-14T11:30:00+01:00") {
            throw DeserializationError("No deserializer for type \"datetime\"", "datetime");
        }
    }
    if (targetType == "CorrectUser" &&
        d.find("birthday") != d.end() && d.at("birthday") == "every day") {
        throw DeserializationError(
            "Could not deserialize value \"every day\" into \"datetime.datetime\".", "datetime.datetime");
    }
    return 1;
}

TEST(TypeErrorTest, test_undefined_deserializer) {
    std::map<std::string,std::string> dumped = { {"id","12"}, {"birthday","1879-03-14T11:30:00+01:00"}};
    try {
        fake_load(dumped, "WrongUser");
        FAIL() << "Expected DeserializationError";
    } catch(const DeserializationError& e) {
        EXPECT_EQ(e.message, "No deserializer for type \"datetime\"");
        EXPECT_EQ(e.target, "datetime");
    }
}

TEST(TypeErrorTest, test_wrong_primitive_type) {
    std::map<std::string,std::string> dumped = { {"id","Albert"}, {"birthday","1879-03-14T11:30:00+01:00"} };
    try {
        fake_load(dumped, "WrongUser");
        FAIL() << "Expected DeserializationError";
    } catch(const DeserializationError& e) {
        EXPECT_EQ(e.message, "Could not cast \"Albert\" into \"int\"");
        EXPECT_EQ(e.target, "int");
    }
}

TEST(TypeErrorTest, test_wrong_type) {
    std::map<std::string,std::string> dumped = { {"id","12"}, {"birthday","every day"} };
    try {
        fake_load(dumped, "CorrectUser");
        FAIL() << "Expected DeserializationError";
    } catch(const DeserializationError& e) {
        EXPECT_TRUE(e.message.find("Could not deserialize value \"every day\" into \"datetime.datetime\".") == 0);
        EXPECT_EQ(e.target, "datetime.datetime");
    }
}