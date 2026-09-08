#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <vector>
#include <string>

// Simple in-memory JsonLines reader/writer for "extra" tests, mimicking iterator interface.
class JsonLinesWriter {
public:
    JsonLinesWriter(std::ostream &out) : out(out) {}
    void write(const nlohmann::json &obj) { out << obj.dump() << "\n"; }
private:
    std::ostream &out;
};

class JsonLinesReader {
public:
    JsonLinesReader(std::istream &in) : in(in) {}

    class iterator {
    public:
        iterator() : in(nullptr), end(true) {}
        iterator(std::istream *in_) : in(in_), end(false) { ++(*this); }
        nlohmann::json operator*() const { return curr; }
        iterator& operator++() {
            std::string line;
            while (std::getline(*in, line)) {
                if (line.empty() || line.find_first_not_of(" \t") == std::string::npos) continue;
                curr = nlohmann::json::parse(line);
                return *this;
            }
            end = true;
            in = nullptr;
            return *this;
        }
        bool operator==(const iterator &rhs) const { return (end && rhs.end) || (in == rhs.in); }
        bool operator!=(const iterator &rhs) const { return !(*this == rhs); }
    private:
        std::istream *in = nullptr;
        nlohmann::json curr;
        bool end = false;
    };
    iterator begin() { return iterator(&in); }
    iterator end()   { return iterator(); }
private:
    std::istream &in;
};

TEST(JsonLinesExtraTest, WriterAndReaderIterateAllLines) {
    std::stringstream ss;
    JsonLinesWriter writer(ss);
    std::vector<nlohmann::json> content = {{"a", 1}, {"b", 2}, {"c", -1}};
    for (const auto &obj : content) writer.write(obj);

    ss.seekg(0);
    JsonLinesReader reader(ss);
    std::vector<nlohmann::json> result;
    for (auto v : reader) {
        result.push_back(v);
    }
    ASSERT_EQ(content, result);
}

TEST(JsonLinesExtraTest, ReaderSkipsBlankLines) {
    std::stringstream ss("\n{\"foo\": 9}\n\n{\"bar\": 7}\n");
    JsonLinesReader reader(ss);
    std::vector<nlohmann::json> got;
    for (auto v : reader)
        got.push_back(v);
    ASSERT_EQ(got.size(), 2);
    ASSERT_EQ(got[0], nlohmann::json({{"foo", 9}}));
    ASSERT_EQ(got[1], nlohmann::json({{"bar", 7}}));
}

TEST(JsonLinesExtraTest, ReaderIgnoresWhitespaceOnlyLines) {
    std::stringstream ss("  \n{\"one\": 1}\n\t  \n{\"two\":2}");
    JsonLinesReader reader(ss);
    std::vector<nlohmann::json> got;
    for (auto v : reader)
        got.push_back(v);
    ASSERT_EQ(got.size(), 2);
    ASSERT_EQ(got[0], nlohmann::json({{"one", 1}}));
    ASSERT_EQ(got[1], nlohmann::json({{"two", 2}}));
}