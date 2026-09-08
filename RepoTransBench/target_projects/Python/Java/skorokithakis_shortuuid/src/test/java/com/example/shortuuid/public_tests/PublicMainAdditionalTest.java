package com.example.shortuuid.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.example.shortuuid.Main;
import com.example.shortuuid.ShortUUID;

import java.util.UUID;
import java.util.List;

public class PublicMainAdditionalTest {

    @Test
    void testEncodeDecodeIntPublic() {
        UUID u = UUID.fromString("12345678-1234-5678-1234-567812345678");
        String encoded = Main.encode(u);
        UUID decoded = Main.decode(encoded);
        assertNotNull(encoded);
        assertTrue(encoded instanceof String);
        assertEquals(u, decoded);
    }

    @Test
    void testUuidLengthChangePublic() {
        String result = Main.uuid(6);
        assertEquals(6, result.length());
    }

    @Test
    void testRandomAlphabetPublic() {
        String alphabet = "xyz123uvw";
        Main.setAlphabet(alphabet);
        String randStr = Main.random(8);
        for (char c : randStr.toCharArray()) {
            assertTrue(alphabet.indexOf(c) >= 0);
        }
        assertEquals(8, randStr.length());
        assertEquals(alphabet, Main.getAlphabet());
    }

    @Test
    void testShortuuidInstanceRandomPublic() {
        String alphabet = "gfedcba098";
        ShortUUID sq = new ShortUUID(alphabet);
        String val = sq.random(7);
        assertEquals(7, val.length());
        for(char c : val.toCharArray()) {
            assertTrue(alphabet.indexOf(c) >= 0);
        }
    }

    @Test
    void testShortuuidInstanceUuidLengthPublic() {
        ShortUUID sq = new ShortUUID("HIJK4567LMN");
        String val = sq.uuid(10);
        assertEquals(10, val.length());
    }

    @Test
    void testShortuuidEncodeDecodeLargeIntPublic() {
        ShortUUID sq = new ShortUUID();
        long num = 312319019L;
        UUID u = new UUID(0, num);
        String encoded = sq.encode(u);
        UUID decoded = sq.decode(encoded);
        assertNotNull(encoded);
        assertEquals(u, decoded);
    }
}