// C++ translation of examples/protocol/test_netstrings.py
#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <stdexcept>

// Simulate important types and basic netstring functionality

struct NetstringSender {
    std::string out;
    NetstringSender() : out("") {}
    void sendNetstring(const std::string& s) {
        std::stringstream ss;
        ss << s.size() << ":" << s << ",";
        out += ss.str();
    }
};

TEST(NetstringTests, SendEmptyNetstring) {
    NetstringSender sender;
    sender.sendNetstring("");
    ASSERT_EQ(sender.out, "0:,");
}

TEST(NetstringTests, SendOneNetstring) {
    NetstringSender sender;
    sender.sendNetstring("foobar");
    ASSERT_EQ(sender.out, "6:foobar,");
}

TEST(NetstringTests, SendTwoNetstrings) {
    NetstringSender sender;
    sender.sendNetstring("spam");
    sender.sendNetstring("egggs");
    ASSERT_EQ(sender.out, "4:spam,5:egggs,");
}

struct FakeReceiver {
    FakeReceiver() : connected(false), lossReason("") { }
    bool connected;
    std::string lossReason;
    std::vector<std::string> netstrings;
    void netstringReceived(const std::string& s) { netstrings.push_back(s); }
    void prepareParsing() { connected = true; }
    void finishParsing(const std::string& reason) { lossReason = reason; }
};

TEST(NetstringTests, EstablishingConnection) {
    FakeReceiver receiver;
    receiver.prepareParsing();
    ASSERT_TRUE(receiver.connected);
}

TEST(NetstringTests, LosingConnection) {
    FakeReceiver receiver;
    receiver.prepareParsing();
    receiver.finishParsing("DISCONNECT");
    ASSERT_EQ(receiver.lossReason, "DISCONNECT");
}