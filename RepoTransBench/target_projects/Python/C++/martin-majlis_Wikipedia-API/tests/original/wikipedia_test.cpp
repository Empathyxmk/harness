#include <gtest/gtest.h>
#include <stdexcept>
#include "wikipedia_api_mock.h"

// TestWikipedia mapped from Python unittest
class TestWikipedia : public ::testing::Test {};

TEST_F(TestWikipedia, MissingUserAgentShouldFail) {
    try {
        Wikipedia wiki("en");
        FAIL() << "Expected assertion throw for missing user agent";
    } catch (const std::invalid_argument& e) {
        std::string expected =
            "Please, be nice to Wikipedia and specify user agent - "
            "https://meta.wikimedia.org/wiki/User-Agent_policy. "
            "Current user_agent: 'en' is not sufficient. "
            "Use Wikipedia(user_agent='your-user-agent', language='en')";
        ASSERT_EQ(std::string(e.what()), expected);
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestWikipedia, SwappedParametersInConstructor) {
    try {
        Wikipedia wiki("en", "my-user-agent");
        FAIL() << "Expected assertion throw for missing user agent";
    } catch (const std::invalid_argument& e) {
        std::string expected =
            "Please, be nice to Wikipedia and specify user agent - "
            "https://meta.wikimedia.org/wiki/User-Agent_policy. "
            "Current user_agent: 'en' is not sufficient. "
            "Use Wikipedia(user_agent='your-user-agent', language='en')";
        ASSERT_EQ(std::string(e.what()), expected);
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestWikipedia, EmptyParametersInConstructor) {
    try {
        Wikipedia wiki("", "");
        FAIL() << "Expected assertion throw for missing user agent";
    } catch (const std::invalid_argument& e) {
        std::string expected =
            "Please, be nice to Wikipedia and specify user agent - "
            "https://meta.wikimedia.org/wiki/User-Agent_policy. "
            "Current user_agent: '' is not sufficient. "
            "Use Wikipedia(user_agent='your-user-agent', language='your-language')";
        ASSERT_EQ(std::string(e.what()), expected);
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestWikipedia, EmptyLanguageInConstructor) {
    try {
        Wikipedia wiki("test-user-agent", "");
        FAIL() << "Expected assertion throw for missing language";
    } catch (const std::invalid_argument& e) {
        std::string expected =
            "Specify language. Current language: '' is not sufficient. "
            "Use Wikipedia(user_agent='test-user-agent', language='your-language')";
        ASSERT_EQ(std::string(e.what()), expected);
    } catch (...) {
        FAIL() << "Expected std::invalid_argument";
    }
}

TEST_F(TestWikipedia, LongLanguageAndUserAgent) {
    Wikipedia wiki("param-user-agent", "very-long-language");
    ASSERT_NE(&wiki, nullptr);
    ASSERT_EQ(wiki.language(), "very-long-language");
    ASSERT_EQ(wiki.variant(), "");
}

TEST_F(TestWikipedia, UserAgentIsUsed) {
    Wikipedia wiki("param-user-agent");
    ASSERT_NE(&wiki, nullptr);
    std::string user_agent = wiki.get_session_headers().at("User-Agent");
    ASSERT_EQ(user_agent, "param-user-agent (" + std::string(USER_AGENT) + ")");
    ASSERT_EQ(wiki.language(), "en");
}

TEST_F(TestWikipedia, UserAgentInHeadersIsFine) {
    Headers hdr = {{"User-Agent", "header-user-agent"}};
    Wikipedia wiki("en", hdr);
    ASSERT_NE(&wiki, nullptr);
    std::string user_agent = wiki.get_session_headers().at("User-Agent");
    ASSERT_EQ(user_agent, "header-user-agent (" + std::string(USER_AGENT) + ")");
}

TEST_F(TestWikipedia, UserAgentInHeadersWin) {
    Headers hdr = {{"User-Agent", "header-user-agent"}};
    Wikipedia wiki("param-user-agent", hdr);
    ASSERT_NE(&wiki, nullptr);
    std::string user_agent = wiki.get_session_headers().at("User-Agent");
    ASSERT_EQ(user_agent, "header-user-agent (" + std::string(USER_AGENT) + ")");
}