#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <vector>
#include <string>

// Simulate public API: writing and reading json lines to/from text streams.

class JsonLinesWriter {
public:
    JsonLinesWriter(std::ostream &out) : out(out) {}
    void write(const nlohmann::json &obj) { out << obj.dump() << "\n"; }
};

class JsonLinesReader {
public:
    JsonLinesReader(std::istream &in) : in(in) {}

    std::vector<nlohmann::json> read_all() {
        std::vector<nlohmann::json> result;
        std::string line;
        while (std::getline(in, line)) {
            if (line.empty() || line.find_first_not_of(" \t\n\r") == std::string::npos) continue;
            result.push_back(nlohmann::json::parse(line));
        }
        return result;
    }
private:
    std::istream &in;
};

TEST(PublicJsonLinesTest, WriteAndReadBack) {
    std::stringstream ss;
    JsonLinesWriter writer(ss);
    std::vector<nlohmann::json> items = {
        {{"id", 1}, {"val", "foo"}},
        {{"id", 2}, {"val", "bar"}}
    };
    for (const auto &item : items)
        writer.write(item);

    ss.seekg(0); // rewind for reading
    JsonLinesReader reader(ss);
    auto read = reader.read_all();
    ASSERT_EQ(read, items);
}

TEST(PublicJsonLinesTest, IgnoresEmptyOrWhitespaceLines) {
    std::stringstream ss("  \n{\"ok\":1}\n\t\n\n   \n{\"cool\":true}\n");
    JsonLinesReader reader(ss);
    auto got = reader.read_all();
    ASSERT_EQ(got.size(), 2);
    ASSERT_EQ(got[0], nlohmann::json({{"ok", 1}}));
    ASSERT_EQ(got[1], nlohmann::json({{"cool", true}}));
}