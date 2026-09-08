package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class StorageFileNotFoundExceptionPublicTest {

    @Test
    void testMessageConstructorPublic() {
        StorageFileNotFoundException ex = new StorageFileNotFoundException("public-message");
        assertEquals("public-message", ex.getMessage());
    }

    @Test
    void testMessageAndCauseConstructorPublic() {
        Throwable cause = new Exception("different-inner");
        StorageFileNotFoundException ex = new StorageFileNotFoundException("different-outer", cause);
        assertEquals("different-outer", ex.getMessage());
        assertEquals(cause, ex.getCause());
    }
}