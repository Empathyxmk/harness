package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class StorageFileNotFoundExceptionTest {

    @Test
    void testMessageConstructor() {
        StorageFileNotFoundException ex = new StorageFileNotFoundException("testmsg");
        assertEquals("testmsg", ex.getMessage());
    }

    @Test
    void testMessageAndCauseConstructor() {
        Throwable cause = new Exception("inner");
        StorageFileNotFoundException ex = new StorageFileNotFoundException("outer", cause);
        assertEquals("outer", ex.getMessage());
        assertEquals(cause, ex.getCause());
    }
}