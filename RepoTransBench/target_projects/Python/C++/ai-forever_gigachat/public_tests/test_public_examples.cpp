#include <gtest/gtest.h>
#include <string>
#include <map>

class SimpleExample {
public:
    std::string q;
    std::string a;
    SimpleExample(const std::string &_q, const std::string &_a) : q(_q), a(_a) {}
    std::string str() const { return "Q: " + q + "\nA: " + a; }
    std::string repr() const { return "SimpleExample(\"" + q + "\", \"" + a + "\")"; }
};

class SimpleFunctionExample {
public:
    std::string fn;
    std::map<std::string, int> params;
    std::string out;
    SimpleFunctionExample(const std::string &_fn, std::map<std::string, int> _params, const std::string &_out)
        : fn(_fn), params(_params), out(_out) {}
    std::string str() const {
        return "Function: " + fn + ", params: ..., output: " + out;
    }
    std::string repr() const {
        return "SimpleFunctionExample(\"" + fn + "\", <params>, \"" + out + "\")";
    }
};

TEST(PublicExamplesTest, SimpleExampleReprAndStr) {
    SimpleExample se("Who created the Eiffel Tower?", "Gustave Eiffel built it in Paris.");
    ASSERT_TRUE(se.q.find("Who created") == 0);
    ASSERT_TRUE(se.a.find("Paris.") == se.a.size() - 6);
    ASSERT_TRUE(se.repr().find("Eiffel") != std::string::npos);
}

TEST(PublicExamplesTest, SimpleFunctionExampleReprAndStr) {
    std::map<std::string, int> params = {{"city", 1}, {"year", 2022}};
    SimpleFunctionExample sfe("weather", params, "performed");
    ASSERT_EQ(sfe.fn, "weather");
    ASSERT_TRUE(sfe.params.find("city") != sfe.params.end());
    ASSERT_EQ(sfe.out, "performed");
}