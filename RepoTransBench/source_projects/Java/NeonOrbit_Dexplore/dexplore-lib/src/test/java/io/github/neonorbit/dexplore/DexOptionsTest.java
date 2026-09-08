package io.github.neonorbit.dexplore;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;

class DexOptionsTest {

    @Test
    void testDefaultOptions() {
        DexOptions options = DexOptions.getDefault();
        assertNotNull(options.opcodes);
        assertFalse(options.enableCache);
        assertFalse(options.rootDexOnly);
    }

    @Test
    void testFieldAssignment() {
        DexOptions options = DexOptions.getDefault();
        options.rootDexOnly = true;
        options.enableCache = true;
        assertTrue(options.rootDexOnly);
        assertTrue(options.enableCache);
    }
}