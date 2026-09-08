#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>
struct ResponseSentence {
    std::string type;
    std::map<std::string, std::string> attributes;
    std::string tag;
    static ResponseSentence parse(std::vector<std::string>&& in) {
        if (in[0]=="!done") return {"done",{},(in.size()>1?in[1]:"")};
        if (in[0]=="!re") return {"re",{ {"c","d"} }, "r"};
        if (in[0]=="!trap") return {"trap",{ {"message","z"} }, ""};
        throw std::logic_error("invalid word");
    }
};
TEST(TestResponseSentencePublic, test_done) {
    auto res = ResponseSentence::parse({"!done",".tag=d"});
    EXPECT_EQ(res.type, "done");
}
TEST(TestResponseSentencePublic, test_re_with_tag) {
    auto res = ResponseSentence::parse({"!re",".tag=x"});
    EXPECT_EQ(res.tag, "x");
}
TEST(TestResponseSentencePublic, test_re_with_invalid_word) {
    EXPECT_THROW(ResponseSentence::parse({"!re","-tag=x"}), std::logic_error);
}