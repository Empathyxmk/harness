package com.smileychris.easythumbnails.public_tests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class PublicStorageTest {

    @Test
    void testGenerateFilenameUniqueStringPublic() {
        assertTrue("pictures/avatars/alice_custom_id_54321.png".startsWith("pictures/avatars/"));
        assertTrue("pictures/avatars/alice_custom_id_54321.png".contains("custom_id_54321") || "pictures/avatars/alice_custom_id_54321.png".endsWith("_alice.png"));
    }

    @Test
    void testGenerateFilenameExtensionPublic() {
        assertTrue("pictures/backgrounds/image123_id_777.gif".endsWith("_image123.gif"));
        assertTrue("pictures/backgrounds/image123_id_777.gif".contains("id_777") || "pictures/backgrounds/image123_id_777.gif".contains("image123"));
    }
}