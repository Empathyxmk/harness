package com.example.publictests;

import com.example.underscore.Underscore;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicBasicsTest {
    @Test
    void testIdentityPublic() {
        assertEquals("underscore", Underscore.identity("underscore"));
    }
}