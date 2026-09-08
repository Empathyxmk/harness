#include <gtest/gtest.h>
#include <stdexcept>
#include <string>

struct PyiCloudException : public std::exception {
    std::string message;
    PyiCloudException(const std::string& msg) : message(msg) {}
    const char* what() const noexcept override { return message.c_str(); }
};

struct PyiCloudAPIResponseException : public std::exception {
    std::string reason;
    std::string code;
    bool retry;
    PyiCloudAPIResponseException(const std::string& r, const std::string& c = "", bool rt = false): reason(r), code(c), retry(rt) {}
    std::string str() const {
        std::string s = reason;
        if (!code.empty()) s += " (" + code + ")";
        if (retry) s += " [Retrying]";
        return s;
    }
    const char* what() const noexcept override { return str().c_str(); }
};

struct PyiCloudServiceNotActivatedException : public std::exception {
    std::string reason;
    PyiCloudServiceNotActivatedException(const std::string& r): reason(r) {}
    const char* what() const noexcept override { return reason.c_str(); }
};

struct PyiCloudFailedLoginException : public std::exception {
    std::string reason;
    PyiCloudFailedLoginException(const std::string& r): reason(r) {}
    const char* what() const noexcept override { return reason.c_str(); }
};
struct PyiCloud2SARequiredException : public std::exception {
    std::string email;
    PyiCloud2SARequiredException(const std::string& e): email(e) {}
    std::string str() const { return "Two-step authentication required for account: " + email; }
    const char* what() const noexcept override { return str().c_str(); }
};
struct PyiCloudNoStoredPasswordAvailableException : public std::exception {
    std::string reason;
    PyiCloudNoStoredPasswordAvailableException(const std::string& r): reason(r) {}
    const char* what() const noexcept override { return reason.c_str(); }
};
struct PyiCloudNoDevicesException : public std::exception {
    std::string reason;
    PyiCloudNoDevicesException(const std::string& r): reason(r) {}
    const char* what() const noexcept override { return reason.c_str(); }
};

TEST(ExceptionTest, PyiCloudException) {
    PyiCloudException ex("test");
    EXPECT_STREQ(ex.what(), "test");
}

TEST(ExceptionTest, PyiCloudAPIResponseBasic) {
    PyiCloudAPIResponseException ex("error reason");
    EXPECT_NE(std::string(ex.what()).find("error reason"), std::string::npos);
    EXPECT_EQ(ex.reason, "error reason");
    EXPECT_EQ(ex.code, "");
}

TEST(ExceptionTest, PyiCloudAPIResponseFull) {
    PyiCloudAPIResponseException ex("fail", "42", true);
    auto s = ex.str();
    EXPECT_NE(s.find("fail"), std::string::npos);
    EXPECT_NE(s.find("42"), std::string::npos);
    EXPECT_NE(s.find("Retrying"), std::string::npos);
    EXPECT_EQ(ex.reason, "fail");
    EXPECT_EQ(ex.code, "42");
}

TEST(ExceptionTest, ServiceNotActivated) {
    PyiCloudServiceNotActivatedException ex("reason");
    EXPECT_NE(std::string(ex.what()).find("reason"), std::string::npos);
}

TEST(ExceptionTest, FailedLogin) {
    PyiCloudFailedLoginException ex("login fail");
    EXPECT_NE(std::string(ex.what()).find("login fail"), std::string::npos);
}

TEST(ExceptionTest, TwoSARequired) {
    PyiCloud2SARequiredException ex("email@email.com");
    EXPECT_NE(std::string(ex.what()).find("Two-step authentication required for account: email@email.com"), std::string::npos);
}

TEST(ExceptionTest, NoStoredPassword) {
    PyiCloudNoStoredPasswordAvailableException ex("no password");
    EXPECT_NE(std::string(ex.what()).find("no password"), std::string::npos);
}

TEST(ExceptionTest, NoDevices) {
    PyiCloudNoDevicesException ex("no device");
    EXPECT_NE(std::string(ex.what()).find("no device"), std::string::npos);
}