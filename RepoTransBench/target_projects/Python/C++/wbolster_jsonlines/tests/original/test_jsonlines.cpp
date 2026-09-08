#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <vector>
#include <string>
#include <exception>

// Simulate minimal JsonLinesReader and JsonLinesWriter for in-memory tests
class InvalidLineError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

class JsonLinesWriter {
public:
    JsonLinesWriter(std::ostream &stream) : out(stream), closed(false) {}

    void write(const nlohmann::json &obj) {
        if (closed)
            throw std::runtime_error("write to closed file");
        out << obj.dump() << "\n";
    }

    void write_all(const std::vector<nlohmann::json> &objs) {
        for (const auto &obj : objs) {
            write(obj);
        }
    }

    void close() { closed = true; }

private:
    std::ostream &out;
    bool closed;
};

class JsonLinesReader {
public:
    JsonLinesReader(std::istream &stream) : in(stream), closed(false) {}

    nlohmann::json read() {
        if (closed)
            throw std::runtime_error("read from closed file");
        std::string line;
        if (!std::getline(in, line))
            throw std::out_of_range("EOF");
        if (line.empty() || line.find_first_not_of(" \t\n\r") == std::string::npos)
            throw InvalidLineError("empty or whitespace-only line");
        try {
            return nlohmann::json::parse(line);
        } catch (std::exception &e) {
            throw InvalidLineError(std::string("Invalid JSON: ") + e.what());
        }
    }

    void close() { closed = true; }

    class Iterator {
    public:
        Iterator(JsonLinesReader* reader, bool end = false) : reader(reader), at_end(end) {
            if (!at_end) {
                try {
                    value = reader->read();
                } catch (...) {
                    at_end = true;
                }
            }
        }
        Iterator& operator++() {
            try {
                value = reader->read();
            } catch (...) {
                at_end = true;
            }
            return *this;
        }
        bool operator!=(const Iterator& other) const { return at_end != other.at_end; }
        const nlohmann::json& operator*() const { return value; }
    private:
        JsonLinesReader* reader;
        nlohmann::json value;
        bool at_end;
    };

    Iterator begin() { return Iterator(this); }
    Iterator end() { return Iterator(this, true); }

private:
    std::istream &in;
    bool closed;
};

TEST(JsonLinesTest, WriteAndReadBack) {
    std::stringstream ss;
    JsonLinesWriter writer(ss);
    nlohmann::json obj = { {"a", 1}, {"b", 2} };

    writer.write(obj);

    JsonLinesReader reader(ss);
    nlohmann::json result = reader.read();
    EXPECT_EQ(result, obj);

    // Should get EOF
    EXPECT_THROW(reader.read(), std::out_of_range);
}

TEST(JsonLinesTest, WriteAllAndReadAll) {
    std::stringstream ss;
    std::vector<nlohmann::json> objs = {
        {{"a", 1}},
        {{"b", 2}},
        {{"c", 3}}
    };

    JsonLinesWriter writer(ss);
    writer.write_all(objs);

    JsonLinesReader reader(ss);
    std::vector<nlohmann::json> got;
    for (auto& obj : reader)
        got.push_back(obj);

    EXPECT_EQ(got, objs);
}

TEST(JsonLinesTest, ReaderThrowsOnInvalidLine) {
    std::string input = "{\"x\":1}\nnot_a_json\n";
    std::stringstream ss(input);
    JsonLinesReader reader(ss);

    nlohmann::json x = reader.read();
    EXPECT_EQ(x, nlohmann::json({{"x", 1}}));

    EXPECT_THROW(reader.read(), InvalidLineError);
}

TEST(JsonLinesTest, ReaderThrowsOnBlankLine) {
    std::string input = "{\"x\":1}\n\n{\"y\":2}\n";
    std::stringstream ss(input);
    JsonLinesReader reader(ss);

    EXPECT_NO_THROW(reader.read());
    EXPECT_THROW(reader.read(), InvalidLineError);
}

TEST(JsonLinesTest, WriterThrowsWhenClosed) {
    std::stringstream ss;
    JsonLinesWriter writer(ss);
    writer.close();
    EXPECT_THROW(writer.write({{"a", 1}}), std::runtime_error);
}

TEST(JsonLinesTest, ReaderThrowsWhenClosed) {
    std::string input = "{\"x\":1}\n";
    std::stringstream ss(input);
    JsonLinesReader reader(ss);
    reader.close();
    EXPECT_THROW(reader.read(), std::runtime_error);
}

TEST(JsonLinesTest, CanIterateOverLines) {
    std::string input = "{\"a\":1}\n{\"b\":2}\n";
    std::stringstream ss(input);
    JsonLinesReader reader(ss);

    std::vector<nlohmann::json> expected = {
        {{"a", 1}},
        {{"b", 2}}
    };

    std::vector<nlohmann::json> got;
    for (auto& x : reader)
        got.push_back(x);

    EXPECT_EQ(got, expected);
}