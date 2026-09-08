package io.github.xiaofeidev.round.round;

import org.junit.Test;
import static org.junit.Assert.*;

public class RoundStatusImplPublicTest {

    @Test
    public void testDefaultValues_public() {
        RoundStatusImpl impl = new RoundStatusImpl();
        assertEquals(0f, impl.getRadius(), 0f);
        assertEquals(0f, impl.getTopLeftRadius(), 0f);
        assertEquals(0f, impl.getTopRightRadius(), 0f);
        assertEquals(0f, impl.getBottomRightRadius(), 0f);
        assertEquals(0f, impl.getBottomLeftRadius(), 0f);
        float[] radiusList = impl.getRadiusList();
        assertEquals(8, radiusList.length);
        for (float r : radiusList) {
            assertEquals(0f, r, 0f);
        }
    }

    @Test
    public void testSetRadius_public() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(8.8f);
        assertEquals(8.8f, impl.getRadius(), 0f);
        float[] radiusList = impl.getRadiusList();
        for (float r : radiusList) {
            assertEquals(8.8f, r, 0f);
        }
    }

    @Test
    public void testSetIndividualRadii_public() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(2f);
        impl.setTopLeftRadius(3f);
        impl.setTopRightRadius(4f);
        impl.setBottomRightRadius(5f);
        impl.setBottomLeftRadius(6f);
        assertEquals(2f, impl.getRadius(), 0f);
        assertEquals(3f, impl.getTopLeftRadius(), 0f);
        assertEquals(4f, impl.getTopRightRadius(), 0f);
        assertEquals(5f, impl.getBottomRightRadius(), 0f);
        assertEquals(6f, impl.getBottomLeftRadius(), 0f);

        float[] r = impl.getRadiusList();
        assertEquals(3f, r[0], 0f);
        assertEquals(3f, r[1], 0f);
        assertEquals(4f, r[2], 0f);
        assertEquals(4f, r[3], 0f);
        assertEquals(5f, r[4], 0f);
        assertEquals(5f, r[5], 0f);
        assertEquals(6f, r[6], 0f);
        assertEquals(6f, r[7], 0f);
    }

    @Test
    public void testFillRadius_public() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(2f);
        impl.setTopLeftRadius(3f);
        impl.setTopRightRadius(4f);
        impl.setBottomRightRadius(5f);
        impl.setBottomLeftRadius(6f);
        // set everything to something else, then fill to reset
        impl.setRadius(11f);
        impl.fillRadius();
        float[] list = impl.getRadiusList();
        assertEquals(3f, list[0], 0f);
        assertEquals(3f, list[1], 0f);
        assertEquals(4f, list[2], 0f);
        assertEquals(4f, list[3], 0f);
        assertEquals(5f, list[4], 0f);
        assertEquals(5f, list[5], 0f);
        assertEquals(6f, list[6], 0f);
        assertEquals(6f, list[7], 0f);
    }
}