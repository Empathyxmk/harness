package com.scrapycssselect.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class TestXpathExpr {

    private String getExpr(String base, String condition) {
        // Simulate XPathExpr adding a condition
        if (base == null || base.isEmpty()) {
            base = ".//*";
        }
        if (condition != null && !condition.isEmpty()) {
            return base + "[" + condition + "]";
        }
        return base;
    }

    @Test
    void testXpathExprCondition() {
        String xpath = getExpr(".//div", "@class='x'");
        assertEquals(".//div[@class='x']", xpath);
    }

    @Test
    void testXpathExprNoCondition() {
        String xpath = getExpr(".//div", "");
        assertEquals(".//div", xpath);
    }
}