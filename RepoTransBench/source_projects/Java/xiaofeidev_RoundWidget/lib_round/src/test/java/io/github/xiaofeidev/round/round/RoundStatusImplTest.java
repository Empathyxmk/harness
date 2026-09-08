package io.github.xiaofeidev.round.round;

import org.junit.Test;
import static org.junit.Assert.*;

public class RoundStatusImplTest {

    @Test
    public void testDefaultValues() {
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
    public void testSetRadius() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(5.5f);
        assertEquals(5.5f, impl.getRadius(), 0f);
        float[] radiusList = impl.getRadiusList();
        for (float r : radiusList) {
            assertEquals(5.5f, r, 0f);
        }
    }

    @Test
    public void testSetIndividualRadii() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(1f);
        impl.setTopLeftRadius(2f);
        impl.setTopRightRadius(3f);
        impl.setBottomRightRadius(4f);
        impl.setBottomLeftRadius(5f);
        assertEquals(1f, impl.getRadius(), 0f);
        assertEquals(2f, impl.getTopLeftRadius(), 0f);
        assertEquals(3f, impl.getTopRightRadius(), 0f);
        assertEquals(4f, impl.getBottomRightRadius(), 0f);
        assertEquals(5f, impl.getBottomLeftRadius(), 0f);

        float[] r = impl.getRadiusList();
        assertEquals(2f, r[0], 0f);
        assertEquals(2f, r[1], 0f);
        assertEquals(3f, r[2], 0f);
        assertEquals(3f, r[3], 0f);
        assertEquals(4f, r[4], 0f);
        assertEquals(4f, r[5], 0f);
        assertEquals(5f, r[6], 0f);
        assertEquals(5f, r[7], 0f);
    }

    @Test
    public void testFillRadius() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(1f);
        impl.setTopLeftRadius(2f);
        impl.setTopRightRadius(3f);
        impl.setBottomRightRadius(4f);
        impl.setBottomLeftRadius(5f);
        // set everything to wrong, then fill to reset
        impl.setRadius(9f);
        impl.fillRadius();
        float[] list = impl.getRadiusList();
        assertEquals(2f, list[0], 0f);
        assertEquals(2f, list[1], 0f);
        assertEquals(3f, list[2], 0f);
        assertEquals(3f, list[3], 0f);
        assertEquals(4f, list[4], 0f);
        assertEquals(4f, list[5], 0f);
        assertEquals(5f, list[6], 0f);
        assertEquals(5f, list[7], 0f);
    }

    @Test
    public void testBuilderSetsValues() {
        RoundStatusImpl impl = new RoundStatusImpl.RoundStatusBuilder()
                .setMRadius(1.1f)
                .setMTopLeftRadius(2.2f)
                .setMTopRightRadius(3.3f)
                .setMBottomRightRadius(4.4f)
                .setMBottomLeftRadius(5.5f)
                .build();

        assertEquals(1.1f, impl.getRadius(), 0f);
        assertEquals(2.2f, impl.getTopLeftRadius(), 0f);
        assertEquals(3.3f, impl.getTopRightRadius(), 0f);
        assertEquals(4.4f, impl.getBottomRightRadius(), 0f);
        assertEquals(5.5f, impl.getBottomLeftRadius(), 0f);
    }
}