#include <gtest/gtest.h>
#include <stdexcept>
#include <string>
#include <vector>

// Dummy/stub FindMyiPhoneService for illustration.
// In a real migration, you'd adapt to actual C++ logic or interface.
class FindMyiPhoneService {
public:
    explicit FindMyiPhoneService(const std::string& user)
        : user_(user), device_locked_(false), location_uptodate_(true) {}

    bool playSound(const std::string& device_id) {
        if (device_id.empty())
            throw std::invalid_argument("Device ID is required");
        return true;
    }

    std::string sendMessage(const std::string& device_id, const std::string& message) {
        if (device_id.empty())
            throw std::invalid_argument("Device ID is required");
        if (message.empty())
            throw std::invalid_argument("Message is required");
        return "Message sent: " + message;
    }

    bool lock(const std::string& device_id, const std::string& passcode) {
        if (device_id.empty() || passcode.empty())
            return false;
        device_locked_ = true;
        return true;
    }

    std::string location(const std::string& device_id) {
        if (device_id.empty())
            throw std::invalid_argument("Device ID is required");
        if (!location_uptodate_) throw std::runtime_error("Location not available");
        return "Cupertino, CA";
    }

    void setLocationUptodate(bool value) { location_uptodate_ = value; }
    bool isLocked() const { return device_locked_; }

private:
    std::string user_;
    bool device_locked_;
    bool location_uptodate_;
};

TEST(FindMyiPhoneServiceTest, PlaySoundWorksForValidDevice) {
    FindMyiPhoneService service("user1");
    EXPECT_TRUE(service.playSound("dev123"));
}

TEST(FindMyiPhoneServiceTest, PlaySoundThrowsIfDeviceIdMissing) {
    FindMyiPhoneService service("user2");
    EXPECT_THROW(service.playSound(""), std::invalid_argument);
}

TEST(FindMyiPhoneServiceTest, SendMessageWorksProperly) {
    FindMyiPhoneService service("user3");
    auto result = service.sendMessage("dev999", "Hello Device");
    EXPECT_EQ(result, "Message sent: Hello Device");
}

TEST(FindMyiPhoneServiceTest, SendMessageThrowsIfMessageMissing) {
    FindMyiPhoneService service("user4");
    EXPECT_THROW(service.sendMessage("dev1", ""), std::invalid_argument);
}

TEST(FindMyiPhoneServiceTest, SendMessageThrowsIfDeviceIdMissing) {
    FindMyiPhoneService service("user4");
    EXPECT_THROW(service.sendMessage("", "Content"), std::invalid_argument);
}

TEST(FindMyiPhoneServiceTest, LockDeviceWorks) {
    FindMyiPhoneService service("user5");
    bool locked = service.lock("dev1", "1234");
    EXPECT_TRUE(locked);
    EXPECT_TRUE(service.isLocked());
}

TEST(FindMyiPhoneServiceTest, LockDeviceFailsWithEmptyFields) {
    FindMyiPhoneService service("user6");
    EXPECT_FALSE(service.lock("", "1234"));
    EXPECT_FALSE(service.lock("dev1", ""));
}

TEST(FindMyiPhoneServiceTest, ReturnsLocationForDevice) {
    FindMyiPhoneService service("user7");
    std::string loc = service.location("dev9");
    EXPECT_EQ(loc, "Cupertino, CA");
}

TEST(FindMyiPhoneServiceTest, ThrowsIfLocationUnavailable) {
    FindMyiPhoneService service("user8");
    service.setLocationUptodate(false);
    EXPECT_THROW(service.location("dev0"), std::runtime_error);
}