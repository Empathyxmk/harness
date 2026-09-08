package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import java.util.*;

class UrlsTest {

    static class UrlMap {
        private Map<String, String> map = new HashMap<>();
        void add(String name, String url) { map.put(name, url); }
        String reverse(String name) { return map.get(name); }
    }

    @Test
    void testUrlPatterns() {
        UrlMap urlMap = new UrlMap();
        urlMap.add("newsfeed:issue_list", "/issues/");
        urlMap.add("newsfeed:issue_detail", "/issues/1/");
        urlMap.add("newsfeed:newsletter_subscribe", "/newsletter/subscribe/");
        assertEquals("/issues/", urlMap.reverse("newsfeed:issue_list"));
        assertEquals("/issues/1/", urlMap.reverse("newsfeed:issue_detail"));
        assertEquals("/newsletter/subscribe/", urlMap.reverse("newsfeed:newsletter_subscribe"));
    }
}