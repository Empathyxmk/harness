#include <gtest/gtest.h>
#include <string>
#include <sstream>
#include <stdexcept>

namespace create_tag {

std::string read_version(const std::string& input) {
    // Very naive parser
    const std::string prefix = "__version__ = '";
    auto idx = input.find(prefix);
    if (idx == std::string::npos)
        throw std::invalid_argument("No __version__ found");
    auto start = idx + prefix.size();
    auto end = input.find("'", start);
    return input.substr(start, end - start);
}

int fake_call(const std::string& cmd) {
    // Always succeed
    return 0;
}

void create_tag(const std::string& version, std::ostringstream& out) {
    auto rc = fake_call("git tag --annotate " + version + " --message 'Version " + version + "'");
    if (rc == 0) {
        out << "Added tag for version " << version;
    }
    // else, do nothing
}
}

TEST(CreateTag, ReadVersionReadsVersion) {
    std::string test = "__version__ = '3.9.8'\n";
    ASSERT_EQ(create_tag::read_version(test), "3.9.8");
}

TEST(CreateTag, ReadVersionRaises) {
    std::string not_version = "xyz = '1.2.3'\n";
    ASSERT_THROW(create_tag::read_version(not_version), std::invalid_argument);
}

TEST(CreateTag, CreateTagSuccess) {
    std::ostringstream oss;
    create_tag::create_tag("1.0.TEST", oss);
    ASSERT_TRUE(oss.str().find("Added tag for version 1.0.TEST") != std::string::npos);
}

// Not printing on failure omitted for brevity