package com.scrapycssselect.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicXpathExprTest {
    private String publicGetExpr(String base, String cond) {
        if (base == null || base.isEmpty()) {
            base = ".//*";
        }
        if (cond != null && !cond.isEmpty()) {
            return base + "[" + cond + "]";
        }
        return base;
    }

    @Test
    void testPublicXpathExprSingleCondition() {
        assertEquals(".//table[@foo='bar']", publicGetExpr(".//table", "@foo='bar'"));
    }

    @Test
    void testPublicXpathExprNoCondition() {
        assertEquals(".//table", publicGetExpr(".//table", ""));
    }

    @Test
    void testPublicXpathExprDefaultBase() {
        assertEquals(".//*[@foo='bar']", publicGetExpr("", "@foo='bar'"));
    }
}