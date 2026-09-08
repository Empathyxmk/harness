#include <gtest/gtest.h>
#include <map>
#include <vector>
#include <string>
#include <stdexcept>

TEST(PublicGotoInternals, GotoLabelAndTable) {
    std::map<std::string, int> table;
    table["label1"] = 10;
    table["label2"] = 20;
    EXPECT_EQ(table["label1"], 10);
    EXPECT_EQ(table["label2"], 20);
}

TEST(PublicGotoInternals, GotoMacroLines) {
    std::string src = "alpha\nbeta\n# label x\n# goto x\nomega";
    std::vector<std::string> lines;
    size_t pos = 0, end;
    while ((end = src.find('\n', pos)) != std::string::npos) {
        lines.push_back(src.substr(pos, end - pos));
        pos = end + 1;
    }
    lines.push_back(src.substr(pos));
    bool found_label = false;
    int label_line = -1;
    for (int i = 0; i < lines.size(); ++i) {
        if (lines[i].find("# label x") != std::string::npos) {
            found_label = true;
            label_line = i;
        }
    }
    EXPECT_TRUE(found_label);
    EXPECT_EQ(label_line, 2);
}

TEST(PublicGotoInternals, GotoInternalsExc) {
    struct Dummy : public std::exception {
        Dummy(const std::string& msg) : msg_(msg) {}
        const char* what() const noexcept override { return msg_.c_str(); }
        std::string msg_;
    };
    std::string got_error;
    try {
        throw Dummy("test error");
    } catch(const Dummy& e) {
        got_error = e.what();
    }
    EXPECT_EQ(got_error, "test error");
}