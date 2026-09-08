#include <gtest/gtest.h>
#include <string>
#include <vector>
#include <map>

class ChannelsPublic {
public:
    struct Channel {
        std::string name;
        std::string id;
    };
    ChannelsPublic(const std::string& token) : token(token) {}

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

TEST(TestChannelsPublic, test_valid_ids_return_channel_id) {
    ChannelsPublic ch("public_token");
    std::vector<ChannelsPublic::Channel> mock_channels{
        {"dev", "C333"},
        {"support",  "C444"}
    };
    ch.setChannelsList(mock_channels);
    EXPECT_EQ(ch.get_channel_id("support"), "C444");
}

TEST(TestChannelsPublic, test_invalid_channel_ids_return_none) {
    ChannelsPublic ch("public_token");
    std::vector<ChannelsPublic::Channel> mock_channels{
        {"dev", "C333"},
        {"support",  "C444"}
    };
    ch.setChannelsList(mock_channels);
    EXPECT_EQ(ch.get_channel_id("not_a_channel"), "");
}