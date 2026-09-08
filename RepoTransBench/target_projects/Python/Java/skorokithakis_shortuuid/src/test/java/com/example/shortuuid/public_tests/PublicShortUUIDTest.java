package com.example.shortuuid.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.shortuuid.ShortUUID;
import com.example.shortuuid.Main;

import java.util.UUID;

public class PublicShortUUIDTest {

    @Test
    void testEncodeDiffValuePublic() {
        UUID u = UUID.fromString("11111111-1111-1111-1111-111111111111");
        String encoded = Main.encode(u);
        assertNotNull(encoded);
        UUID decoded = Main.decode(encoded);
        assertEquals(u, decoded);
    }

    @Test
    void testEncodeEmptyPublic() {
        UUID empty = new UUID(0, 0);
        String encoded = Main.encode(empty);
        assertNotNull(encoded);
        assertEquals(empty, Main.decode(encoded));
    }

    @Test
    void testShortuuidUuidLength12Public() {
        ShortUUID sq = new ShortUUID();
        String result = sq.uuid(12);
        assertEquals(12, result.length());
    }

    @Test
    void testShortuuidRandomCharsetPublic() {
        ShortUUID sq = new ShortUUID("XYabc890");
        String r = sq.random(5);
        assertEquals(5, r.length());
        for(char c : r.toCharArray()) {
            assertTrue("XYabc890".indexOf(c) >= 0);
        }
    }

    @Test
    void testShortuuidEncodeDecodeCustomAlphabetPublic() {
        ShortUUID sq = new ShortUUID("abc4321p");
        UUID u = UUID.fromString("deadcafe-1234-4321-aaaa-1111abcdef00");
        String s = sq.encode(u);
        UUID decoded = sq.decode(s);
        assertEquals(u, decoded);
    }

    @Test
    void testShortuuidUuidAndRandomAreDistinctPublic() {
        ShortUUID sq = new ShortUUID();
        String val1 = sq.uuid();
        String val2 = sq.random(val1.length());
        assertNotEquals(val1, val2);
    }
}