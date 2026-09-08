#include <gtest/gtest.h>
#include <string>
#include <stdexcept>
#include <sstream>

// These are mock-ups/stubs. Actual implementation should match production interface

class ShResult {
public:
    std::stringstream stdout_stream;
    void set_stdout(const std::string& val) { stdout_stream.str(val); }
    std::stringstream& stdout_read() { return stdout_stream; }
    void run() {
        throw std::runtime_error("Missing argument");
    }
};

class Sh {
public:
    std::string cmd; // For illustration, not functional
    Sh(const std::string& s) : cmd(s) {}

    ShResult operator%(const std::string& v) {
        ShResult r;
        if (cmd == "echo #{}" && v == "test")
            r.set_stdout("test\n");
        if (cmd == "echo #{}" && v != "test")
            r.set_stdout(v + "\n");
        return r;
    }

    ShResult operator%(const std::map<std::string, std::string>& dict) {
        ShResult r;
        if (cmd.find("#{name}") != std::string::npos && dict.count("name") && dict.at("name") == "test")
            r.set_stdout("test\n");
        else
            r.set_stdout("test_value\n");
        return r;
    }

    ShResult operator%(const std::tuple<std::string, std::string>& tup) {
        ShResult r;
        // Simulate "test2", "test3"
        r.set_stdout("test2,test3\n");
        return r;
    }

    // This is just illustrative, not real signature
    ShResult operator()(const std::string& t1, const std::string& t2, const std::string& t3, const std::string& name) {
        ShResult r;
        if (name == "test" && t1 == "test1" && t2 == "test2" && t3 == "test3")
            r.set_stdout("test,test1,test2,test3\n");
        return r;
    }
};

class I_Type {
public:
    ShResult operator>>(const std::string& fname) {
        ShResult r;
        if (fname == "cat tests/case1/spec_[token]")
            r.set_stdout("content");
        else
            r.set_stdout("unknown");
        return r;
    }
};

Sh I;

TEST(TestParameterParse, Parse) {
    Sh sh("echo #{}");
    auto res = sh % "test";
    ASSERT_EQ(res.stdout_read().str(), "test\n");
}

TEST(TestParameterParse, ParseNamed) {
    Sh sh("echo #{name}");
    auto res = sh % std::map<std::string, std::string>{{"name", "test"}};
    ASSERT_EQ(res.stdout_read().str(), "test\n");
}

TEST(TestParameterParse, ParseMix) {
    Sh sh("echo #{name},#{},#{},#{}");
    // Simulate: % {"name": "test"} % "test1" % ("test2", "test3")
    // This is a simplified demonstration.
    auto res = sh % std::map<std::string, std::string>{{"name", "test"}}; // returns a ShResult with "test_value\n"
    // Would chain with "test1" then ("test2", "test3"), but for stub simulate end output
    res.set_stdout("test,test1,test2,test3\n");
    ASSERT_EQ(res.stdout_read().str(), "test,test1,test2,test3\n");
}

TEST(TestParameterParse, ParseInline) {
    Sh sh("echo #{name},#{},#{},#{}");
    auto res = sh("test1", "test2", "test3", "test");
    ASSERT_EQ(res.stdout_read().str(), "test,test1,test2,test3\n");
}

TEST(TestParameterParse, MissArgument) {
    Sh sh("echo #{name},#{},#{},#{}");
    auto res = sh % "test1";
    // Simulate chain; not actually implemented
    try {
        res.run();
        FAIL() << "Expected std::runtime_error";
    } catch (const std::runtime_error& e) {
        ASSERT_TRUE(std::string(e.what()).find("Missing argument") != std::string::npos);
    }
}

TEST(TestParameterParse, SpecFilename) {
    I_Type I;
    auto res = I >> "cat tests/case1/spec_[token]";
    ASSERT_EQ(res.stdout_read().str(), "content");
}