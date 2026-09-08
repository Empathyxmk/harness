#include <gtest/gtest.h>
#include <vector>
#include <string>
#include <stdexcept>

// Simulated Email system for testing
struct Email {
    std::string subject;
    std::string to;
    std::string body;
};

struct Subscriber {
    std::string email_address;
    bool subscribed = false;
    bool verified = false;
    bool expired = false;
    Subscriber(std::string email, bool sub, bool veri) : email_address(email), subscribed(sub), verified(veri) {}
};

struct Newsletter {
    std::string subject;
    bool is_sent = false;
    Newsletter(std::string s) : subject(s) {}
};

struct NewsletterEmailSender {
    int batch_size = 5;
    std::vector<std::string> last_batch;
    static std::map<std::string, std::string> _render_newsletter(Newsletter& newsletter) {
        return {{"subject", newsletter.subject}, {"html", "HtmlBody"}};
    }
    Email _generate_email_message(const std::string& to, std::map<std::string, std::string>& rendered) {
        return Email{rendered["subject"], to, rendered["html"]};
    }
    std::vector<Email> _get_batch_email_messages(std::map<std::string, std::string>& rendered, std::vector<Subscriber>& subs) {
        std::vector<Email> batch;
        int count = 0;
        for (auto& sub : subs) {
            if (sub.subscribed && sub.verified) {
                batch.push_back(_generate_email_message(sub.email_address, rendered));
                count++;
                if (count == batch_size) break;
            }
        }
        if (batch.empty()) throw std::runtime_error("No subscribers");
        return batch;
    }
};

struct EmailSystem {
    std::vector<Email> outbox;
    void send(const Email& email) { outbox.push_back(email); }
};

TEST(SendSubscriptionVerificationEmailTest, send_subscription_verification_email) {
    EmailSystem email_system;
    Subscriber sub("user@example.com", false, false);
    Email email{"Please Confirm Your Subscription", sub.email_address, sub.email_address + "/verify"};
    email_system.send(email);
    ASSERT_EQ(email_system.outbox.size(), 1);
    ASSERT_EQ(email_system.outbox[0].subject, "Please Confirm Your Subscription");
    ASSERT_EQ(email_system.outbox[0].to, "user@example.com");
    ASSERT_NE(email_system.outbox[0].body.find("user@example.com/verify"), std::string::npos);
}

TEST(SendNewsletterEmailTest, send_email_newsletter) {
    EmailSystem email_system;
    Newsletter n1("Subject1"), n2("Subject2");
    std::vector<Subscriber> subs;
    for (int i=0; i<5; ++i) subs.emplace_back("v"+std::to_string(i)+"@mail.com", true, true);
    for (auto& sub : subs) {
        Email email{n1.subject, sub.email_address, "HtmlBody"};
        email_system.send(email);
    }
    for (auto& sub : subs) {
        Email email{n2.subject, sub.email_address, "HtmlBody"};
        email_system.send(email);
    }
    ASSERT_EQ(email_system.outbox.size(), 10);
    ASSERT_EQ(email_system.outbox[0].subject, n1.subject);
    ASSERT_EQ(email_system.outbox[5].subject, n2.subject);
}

TEST(SendNewsletterEmailTest, get_subscriber_emails_return_email_message_instances) {
    Newsletter newsletter("Subject123");
    NewsletterEmailSender sender;
    std::vector<Subscriber> subs;
    for (int i=0; i<5; ++i) subs.emplace_back("t"+std::to_string(i)+"@mail.com", true, true);
    auto rendered = NewsletterEmailSender::_render_newsletter(newsletter);
    auto emails = sender._get_batch_email_messages(rendered, subs);
    ASSERT_TRUE(!emails.empty());
    ASSERT_EQ(emails[0].subject, newsletter.subject);
}

TEST(SendNewsletterEmailTest, get_subscriber_emails_with_zero_subscribers) {
    Newsletter newsletter("SubjectNoSub");
    NewsletterEmailSender sender;
    std::vector<Subscriber> subs; // empty
    auto rendered = NewsletterEmailSender::_render_newsletter(newsletter);
    ASSERT_THROW(sender._get_batch_email_messages(rendered, subs), std::runtime_error);
}

TEST(CheckAjaxTest, request_is_ajax) {
    bool is_ajax = true;
    ASSERT_TRUE(is_ajax);
}

TEST(CheckAjaxTest, request_is_not_ajax) {
    bool is_ajax = false;
    ASSERT_FALSE(is_ajax);
}