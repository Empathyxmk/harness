import unittest
import requests_oauthlib.compliance_fixes

class TestPublicComplianceFixes(unittest.TestCase):
    def test_facebook_fixes_public(self):
        # Just tests entry point, different from existing test
        fixed = requests_oauthlib.compliance_fixes.facebook.facebook_compliance_fix(lambda x: x)
        self.assertTrue(callable(fixed))

    def test_mailchimp_fixes_public(self):
        fixed = requests_oauthlib.compliance_fixes.mailchimp.mailchimp_compliance_fix(lambda x: x)
        self.assertTrue(callable(fixed))

    def test_fitbit_fixes_public(self):
        fixed = requests_oauthlib.compliance_fixes.fitbit.fitbit_compliance_fix(lambda x: x)
        self.assertTrue(callable(fixed))

    def test_slack_fixes_public(self):
        fixed = requests_oauthlib.compliance_fixes.slack.slack_compliance_fix(lambda x: x)
        self.assertTrue(callable(fixed))