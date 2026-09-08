package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class StoragePropertiesTest {
    @Test
    void testDefaultLocation() {
        StorageProperties properties = new StorageProperties();
        assertEquals("uploads", properties.getLocation());
    }

    @Test
    void testSetLocation() {
        StorageProperties properties = new StorageProperties();
        properties.setLocation("abc");
        assertEquals("abc", properties.getLocation());
    }
}