package com.example.shortuuid.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

import com.example.shortuuid.*;

public class PublicShortUUIDInitImportsTest {

    @Test
    void testShortuuidImportMainPublic() {
        assertNotNull(ShortUUID.class);
        assertNotNull(Main.encode(UUID.randomUUID()));
        assertNotNull(Main.decode(Main.encode(UUID.randomUUID())));
        assertNotNull(Main.uuid());
    }
}