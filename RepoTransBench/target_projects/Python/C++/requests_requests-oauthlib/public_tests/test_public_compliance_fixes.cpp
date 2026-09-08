#include <gtest/gtest.h>
#include "requests_oauthlib/compliance_fixes.h"
using namespace compliance_fixes;

TEST(TestPublicComplianceFixes, FacebookFixesPublic) {
    auto fn = facebook_compliance_fix([](int x) { return true; });
    EXPECT_TRUE(fn(0));
}

TEST(TestPublicComplianceFixes, MailchimpFixesPublic) {
    auto fn = mailchimp_compliance_fix([](int x) { return true; });
    EXPECT_TRUE(fn(1));
}

TEST(TestPublicComplianceFixes, FitbitFixesPublic) {
    auto fn = fitbit_compliance_fix([](int x) { return false; });
    EXPECT_FALSE(fn(2));
}

TEST(TestPublicComplianceFixes, SlackFixesPublic) {
    auto fn = slack_compliance_fix([](int x) { return true; });
    EXPECT_TRUE(fn(3));
}