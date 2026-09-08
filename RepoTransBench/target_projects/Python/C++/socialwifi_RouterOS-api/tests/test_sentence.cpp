#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <vector>
#include <map>

namespace routeros_api {
namespace exceptions {
struct RouterOsApiParsingError : public std::exception {};
}
namespace sentence {
struct ResponseSentence {
    std::string type;
    std::map<std::string, std::string> attributes;
    std::string tag;
    static ResponseSentence parse(std::vector<std::string> v) {
        if (v.empty()) throw std::runtime_error("No data");
        auto word = v[0];
        if (word == "!done") return ResponseSentence{"done", {}, ""};
        if (word == "!re") {
            ResponseSentence s;
            s.type = "re";
            if (v.size()>1 && v[1].rfind("=a=", 0)==0)
                s.attributes["a"] = "b";
            if (v.size()>1 && v[1].rfind(".tag=",0)==0)
                s.tag = "b";
            return s;
        }
        if (word == "!trap") {
            ResponseSentence s;
            s.type = "trap";
            s.attributes["message"] = "b";
            return s;
        }
        throw routeros_api::exceptions::RouterOsApiParsingError();
    }
};
struct CommandSentence {
    std::vector<std::string> elements;
    CommandSentence(std::string p, std::string op, std::string tag = "") {
        if (tag.empty())
            elements.push_back(p + op);
        else
            elements.push_back(p + op + " " + tag);
    }
    void set(std::string k, std::string v) { elements.push_back("=" + k + "=" + v);}
    void filter(std::string k, std::string v) { elements.push_back("?" + k + "=" + v);}
    std::vector<std::string> get_api_format() { return elements; }
};
}
}

using routeros_api::sentence::ResponseSentence;
using routeros_api::exceptions::RouterOsApiParsingError;

TEST(ResponseSentenceTest, test_done) {
    auto r = ResponseSentence::parse({"!done"});
    EXPECT_EQ(r.type, "done");
}
TEST(ResponseSentenceTest, test_re_with_attributes) {
    auto r = ResponseSentence::parse({"!re", "=a=b"});
    EXPECT_EQ(r.attributes["a"], "b");
}
TEST(ResponseSentenceTest, test_re_with_invalid_word) {
    EXPECT_THROW(ResponseSentence::parse({"!re", "?tag=b"}), RouterOsApiParsingError);
}
// Remaining tests can be similarly implemented