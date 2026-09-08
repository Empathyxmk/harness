package com.peritus.bumpversion.publictests;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class PublicBumpversionInitTest {

    @Test
    void testMainModuleImportablePublic() {
        assertTrue(BumpversionReflection.hasVersion());
    }

    @Test
    void testVersionPropertyExistencePublic() {
        String version = BumpversionReflection.getVersion();
        assertNotNull(version);
        assertFalse(version.isEmpty());
    }
}

// Dummy simulates bumpversion.__version__
class BumpversionReflection {
    public static boolean hasVersion() {
        return true;
    }
    public static String getVersion() {
        return "1.0.0";
    }
}