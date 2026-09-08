package net.vatri.ecommerce.storage;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class StoragePropertiesPublicTest {
    @Test
    void testDefaultLocationPublic() {
        StorageProperties properties = new StorageProperties();
        // Use assertNotEquals with old value and set to a different thing after to check
        assertNotEquals("somewhereelse", properties.getLocation());
        assertEquals("uploads", properties.getLocation());
    }

    @Test
    void testSetLocationPublic() {
        StorageProperties properties = new StorageProperties();
        properties.setLocation("my_new_location");
        assertEquals("my_new_location", properties.getLocation());
        assertNotEquals("abc", properties.getLocation());
    }
}