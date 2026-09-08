package removedfonts;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FontExamplePublicTest {

    @Test
    void testGetAvailableFontFamilyNames_public() {
        String[] fontNames = FontExample.getAvailableFontFamilyNames();
        assertNotNull(fontNames);
        // Use a different minimal font check: look for either "Monospaced" or "DialogInput"
        boolean found = false;
        for (String font : fontNames) {
            if ("Monospaced".equals(font) || "DialogInput".equals(font)) {
                found = true;
                break;
            }
        }
        assertTrue(found, "Should have some basic monospace font family available");
    }
}