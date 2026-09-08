package com.example.original;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class AppsTest {

    static class NewsfeedConfig {
        String name = "newsfeed";
        String verboseName = "News Feed";
        String getName() { return name; }
        String getVerboseName() { return verboseName; }
    }

    @Test
    void testAppsConfigName() {
        NewsfeedConfig config = new NewsfeedConfig();
        assertEquals("newsfeed", config.getName());
    }

    @Test
    void testAppsConfigVerboseName() {
        NewsfeedConfig config = new NewsfeedConfig();
        assertEquals("News Feed", config.getVerboseName());
    }
}