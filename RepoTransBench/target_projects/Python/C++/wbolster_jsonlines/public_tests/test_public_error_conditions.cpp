#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <stdexcept>
#include <string>

class InvalidLineError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

class JsonLinesWriter {
public:
    JsonLinesWriter(std::ostream &out) : out(out), closed(false) {}
    void write(const nlohmann::json &obj) {
        if (closed)
            throw std::runtime_error("file is closed");
        out << obj.dump() << "\n";
    }
    void close() { closed = true; }
private:
    std::ostream &out;
    bool closed;
};

class JsonLinesReader {
public:
    JsonLinesReader(std::istream &in) : in(in), closed(false) {}
    nlohmann::json read() {
        if (closed)
            throw std::runtime_error("file is closed");
        std::string line;
        if (!std::getline(in, line))
            throw std::out_of_range("eof");
        if (line.find_first_not_of(" \t\n\r") == std::string::npos)
            throw InvalidLineError("blank line");
        try {
            return nlohmann::json::parse(line);
        } catch (std::exception &e) {
            throw InvalidLineError(e.what());
        }
    }
    void close() { closed = true; }
private:
    std::istream &in;
    bool closed;
};

TEST(PublicErrorConditionsTest, WriterClosedThrows) {
    std::stringstream ss;
    JsonLinesWriter writer(ss);
    writer.close();
    EXPECT_THROW(writer.write({{"foo", 1}}), std::runtime_error);
}

TEST(PublicErrorConditionsTest, ReaderClosedThrows) {
    std::stringstream ss("  {\"alpha\": 1}\n ");
    JsonLinesReader reader(ss);
    reader.close();
    EXPECT_THROW(reader.read(), std::runtime_error);
}

TEST(PublicErrorConditionsTest, ReaderThrowsOnInvalidLine) {
    std::stringstream ss("{\"ok\": 1}\n  {this is not json}\n{\"z\":9}\n");
    JsonLinesReader reader(ss);

    auto valid1 = reader.read();
    EXPECT_EQ(valid1, nlohmann::json({{"ok", 1}}));

    EXPECT_THROW(reader.read(), InvalidLineError);
    // Next valid line should parse after error
    auto valid2 = reader.read();
    EXPECT_EQ(valid2, nlohmann::json({{"z", 9}}));
}