package com.aiforever.gigachat.original;

import org.junit.jupiter.api.Test;
import java.util.*;
import static org.junit.jupiter.api.Assertions.*;

class ThreadObj {
    String id;
    String title;
    int msgCount;

    public ThreadObj(String id, String title, int msgCount) {
        this.id = id;
        this.title = title;
        this.msgCount = msgCount;
    }
}

public class PublicThreadsTest {
    @Test
    void testThreadObjFields() {
        ThreadObj t = new ThreadObj("th100", "Welcome Thread", 5);
        assertEquals("th100", t.id);
        assertEquals("Welcome Thread", t.title);
        assertEquals(5, t.msgCount);
    }

    @Test
    void testThreadMessageLogic() {
        ThreadObj t = new ThreadObj("th202", "Q&A", 0);
        t.msgCount++;
        assertEquals(1, t.msgCount);
    }
}