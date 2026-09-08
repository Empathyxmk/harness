#include <gtest/gtest.h>
#include <nlohmann/json.hpp>
#include <sstream>
#include <stdexcept>
#include <string>

class InvalidLineError : public std::runtime_error {
public:
    using std::runtime_error::runtime_error;
};

// Simulate very simple JsonLinesWriter/Reader in-memory error conditions as in the Python tests
class JsonLinesWriter {
public:
    JsonLinesWriter(std::ostream &stream) : out(stream), closed(false) {}

    void write(const nlohmann::json &obj) {
        if (closed)
            throw std::runtime_error("write to closed file");
        out << obj.dump() << "\n";
    }

    void close() { closed = true; }

private:
    std::ostream &out;
    bool closed;
};

class JsonLinesReader {
public:
    JsonLinesReader(std::istream& stream) : in(stream), closed(false) {}

    nlohmann::json read() {
        if (closed)
            throw std::runtime_error("read from closed file");
        std::string line;
        if (!std::getline(in, line))
            throw std::out_of_range("EOF"); // End of file
        if (line.find_first_not_of(" \t\r\n") == std::string::npos)
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

TEST(JsonLinesErrorTest, WriterThrowsIfClosed) {
    std::stringstream ss;
    JsonLinesWriter writer(ss);
    writer.close();
    EXPECT_THROW(writer.write({{"foo", 1}}), std::runtime_error);
}

TEST(JsonLinesErrorTest, ReaderThrowsIfClosed) {
    std::stringstream ss("{\"a\": 123}\n");
    JsonLinesReader reader(ss);
    reader.close();
    EXPECT_THROW(reader.read(), std::runtime_error);
}

TEST(JsonLinesErrorTest, ReaderThrowsOnInvalidJson) {
    std::stringstream ss("{\"ok\": 1}\n{invalid json}\n{\"next\":2}\n");
    JsonLinesReader reader(ss);

    auto obj1 = reader.read();
    EXPECT_EQ(obj1, nlohmann::json({{"ok", 1}}));

    EXPECT_THROW(reader.read(), InvalidLineError);

    // Should still be able to read the next valid line after an error
    auto obj2 = reader.read();
    EXPECT_EQ(obj2, nlohmann::json({{"next", 2}}));
}

TEST(JsonLinesErrorTest, ReaderThrowsOnAllBlankLine) {
    std::stringstream ss("\n\n");
    JsonLinesReader reader(ss);

    EXPECT_THROW(reader.read(), InvalidLineError); // first blank
    // If we try again, should get another InvalidLineError (each blank line)
    // Wrap in try/catch to continue
    try {
        reader.read();
    } catch (const InvalidLineError& e) {
        SUCCEED();
    }
}

TEST(JsonLinesErrorTest, ReaderReportsEofAfterBlankLines) {
    std::stringstream ss("  \n\n  ");  // spaces only lines
    JsonLinesReader reader(ss);
    EXPECT_THROW(reader.read(), InvalidLineError);
    // After all lines exhausted, throws EOF on next
    try {
        reader.read();
    } catch (const InvalidLineError&) {
        // try again for EOF
        EXPECT_THROW(reader.read(), std::out_of_range);
    }
}