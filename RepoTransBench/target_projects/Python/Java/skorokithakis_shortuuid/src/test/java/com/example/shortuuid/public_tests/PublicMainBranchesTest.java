package com.example.shortuuid.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.shortuuid.ShortUUID;

import java.util.UUID;

public class PublicMainBranchesTest {

    @Test
    void testShortuuidDifferentAlphabetBranchPublic() {
        ShortUUID sq = new ShortUUID("mnop5678");
        String shortid = sq.random(4);
        assertEquals(4, shortid.length());
        for(char c : shortid.toCharArray()) {
            assertTrue("mnop5678".indexOf(c) >= 0);
        }
    }

    @Test
    void testShortuuidEmptyAlphabetRaisesPublic() {
        assertThrows(IllegalArgumentException.class, () -> new ShortUUID(""));
    }

    @Test
    void testShortuuidRandomSameLengthPublic() {
        ShortUUID sq = new ShortUUID();
        String s1 = sq.random(6);
        String s2 = sq.random(6);
        assertEquals(6, s1.length());
        assertEquals(6, s2.length());
    }

    @Test
    void testShortuuidEncodeDecodeSpecialPublic() {
        ShortUUID sq = new ShortUUID();
        UUID u = UUID.fromString("11111111-2222-3333-4444-555555555555");
        String encoded = sq.encode(u);
        UUID decoded = sq.decode(encoded);
        assertEquals(u, decoded);
    }

    @Test
    void testShortuuidCopyInstancePublic() {
        ShortUUID orig = new ShortUUID("azAZQW12");
        ShortUUID copy = new ShortUUID(orig.getAlphabet());
        assertEquals(orig.getAlphabet(), copy.getAlphabet());
    }
}