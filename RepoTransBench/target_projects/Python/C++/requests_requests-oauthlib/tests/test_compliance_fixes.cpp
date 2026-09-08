#include <gtest/gtest.h>
#include "requests_oauthlib/compliance_fixes.h"

using namespace compliance_fixes;

TEST(FacebookComplianceFixTest, EntryPointCallable) {
    auto fn = facebook_compliance_fix([](int x) { return true; });
    EXPECT_TRUE(fn(123));
}

TEST(MailchimpComplianceFixTest, EntryPointCallable) {
    auto fn = mailchimp_compliance_fix([](int x) { return true; });
    EXPECT_TRUE(fn(42));
}

// Add for fitbit, slack, etc. Replicate all fix entry point and flow tests.