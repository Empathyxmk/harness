package me.drakeet.floo;

import org.junit.Test;
import static org.junit.Assert.*;

public class TargetMapPublicTest {

    @Test
    public void testPutAndGet_public() {
        TargetMap map = new TargetMap();
        map.put("/my/path", "targetValue");
        assertEquals("targetValue", map.get("/my/path"));
    }

    @Test
    public void testGetNonExistingKey_public() {
        TargetMap map = new TargetMap();
        assertNull(map.get("/no/such/key"));
    }
}