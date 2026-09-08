#include <gtest/gtest.h>
#include <string>
#include <regex>

class SubscriberEmailForm {
public:
    explicit SubscriberEmailForm(const std::string& email) : valid_(false), email_address_(email) {
        static const std::regex pattern(R"((.+)@(.+)\.(.+))");
        valid_ = std::regex_match(email, pattern);
    }
    bool is_valid() const { return valid_; }
    std::string cleaned_email_address() const { return email_address_; }
    bool has_email_error() const { return !valid_; }
private:
    bool valid_;
    std::string email_address_;
};

TEST(TestSubscriberEmailForm, valid_email) {
    SubscriberEmailForm form("test@example.com");
    ASSERT_TRUE(form.is_valid());
    ASSERT_EQ(form.cleaned_email_address(), "test@example.com");
}

TEST(TestSubscriberEmailForm, invalid_email) {
    SubscriberEmailForm form("not-an-email");
    ASSERT_FALSE(form.is_valid());
    ASSERT_TRUE(form.has_email_error());
}

TEST(TestSubscriberEmailForm, missing_email) {
    SubscriberEmailForm form("");
    ASSERT_FALSE(form.is_valid());
    ASSERT_TRUE(form.has_email_error());
}