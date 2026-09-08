#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <vector>
#include <iterator>

// Similar iterator use as "extra" Python public test

class JsonLinesReader {
public:
    JsonLinesReader(std::istream &in) : in(in) {}

    class iterator : public std::iterator<std::input_iterator_tag, nlohmann::json> {
    public:
        iterator() : in(nullptr), ended(true) {}
        iterator(std::istream *in_) : in(in_), ended(false) { ++(*this); }
        nlohmann::json operator*() const { return curr; }
        iterator& operator++() {
            std::string line;
            while (std::getline(*in, line)) {
                if (line.empty() || line.find_first_not_of(" \t\n\r") == std::string::npos) continue;
                curr = nlohmann::json::parse(line);
                return *this;
            }
            ended = true;
            in = nullptr;
            return *this;
        }
        bool operator==(const iterator& rhs) const {
            return (ended && rhs.ended) || (in == rhs.in);
        }
        bool operator!=(const iterator& rhs) const {
            return !(*this == rhs);
        }
    private:
        std::istream *in = nullptr;
        nlohmann::json curr;
        bool ended = false;
    };
    iterator begin() { return iterator(&in); }
    iterator end() { return iterator(); }

private:
    std::istream &in;
};

TEST(PublicJsonLinesExtraTest, PublicIteratorWorks) {
    std::stringstream ss("{\"a\": 1}\n{\"b\": 2}\n{\"c\": 3}\n");
    JsonLinesReader reader(ss);
    std::vector<nlohmann::json> got;
    for (auto v : reader)
        got.push_back(v);
    ASSERT_EQ(got[0], nlohmann::json({{"a", 1}}));
    ASSERT_EQ(got[1], nlohmann::json({{"b", 2}}));
    ASSERT_EQ(got[2], nlohmann::json({{"c", 3}}));
}