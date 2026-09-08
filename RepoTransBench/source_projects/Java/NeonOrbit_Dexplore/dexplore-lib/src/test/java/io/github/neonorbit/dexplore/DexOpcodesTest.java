package io.github.neonorbit.dexplore;

import org.jf.dexlib2.Opcodes;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class DexOpcodesTest {

    @Test
    void testAutoIsNull() {
        DexOpcodes auto = DexOpcodes.auto();
        assertNull(auto.get());
    }

    @Test
    void testDefault() {
        DexOpcodes defaults = DexOpcodes.getDefault();
        assertNotNull(defaults.get());
        assertEquals(Opcodes.getDefault(), defaults.get());
    }

    @Test
    void testForApi() {
        DexOpcodes apis = DexOpcodes.forApi(20);
        assertNotNull(apis.get());
        assertEquals(Opcodes.forApi(20), apis.get());
    }

    @Test
    void testForArtVersion() {
        DexOpcodes art = DexOpcodes.forArtVersion(123);
        assertNotNull(art.get());
        assertEquals(Opcodes.forArtVersion(123), art.get());
    }

    @Test
    void testForDexVersion() {
        DexOpcodes dex = DexOpcodes.forDexVersion(35);
        assertNotNull(dex.get());
        assertEquals(Opcodes.forDexVersion(35), dex.get());
    }
}