package com.example.wikiapi.publictests;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.Test;

class PublicUtilsAndConstsTest {

    @Test
    void testUserAgentLength() {
        assertTrue(WikipediaApi.USER_AGENT.length() > 10);
    }

    @Test
    void testMinUserAgentLenIsPositive() {
        assertTrue(WikipediaApi.MIN_USER_AGENT_LEN > 0);
    }
}