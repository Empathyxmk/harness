#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>

class Channels {
public:
    struct Channel {
        std::string name;
        std::string id;
    };
    Channels(const std::string& token) : token(token) {}

    // Simulate a channels.list API fetch by storing fake data for test
    void setChannelsList(const std::vector<Channel>& mock_channels) {
        channels_ = mock_channels;
    }
    std::string get_channel_id(const std::string& name) const {
        for (const auto& c : channels_) {
            if (c.name == name) return c.id;
        }
        return "";
    }
private:
    std::string token;
    std::vector<Channel> channels_;
};

TEST(TestChannels, test_valid_ids_return_channel_id) {
    Channels ch("aaa");
    std::vector<Channels::Channel> mock_channels{
        {"general", "C111"},
        {"random",  "C222"}
    };
    ch.setChannelsList(mock_channels);
    EXPECT_EQ(ch.get_channel_id("general"), "C111");
}

TEST(TestChannels, test_invalid_channel_ids_return_none) {
    Channels ch("aaa");
    std::vector<Channels::Channel> mock_channels{
        {"general", "C111"},
        {"random",  "C222"}
    };
    ch.setChannelsList(mock_channels);
    EXPECT_EQ(ch.get_channel_id("fake_group"), "");
}