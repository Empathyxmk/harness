package io.github.xiaofeidev.round.round;

import org.junit.Test;
import static org.junit.Assert.*;

public class RoundStatusPublicTest {

    @Test
    public void testRadiusSettersGetters_public() {
        RoundStatusImpl impl = new RoundStatusImpl();
        impl.setRadius(10f);
        impl.setTopLeftRadius(12f);
        impl.setTopRightRadius(13f);
        impl.setBottomRightRadius(14f);
        impl.setBottomLeftRadius(15f);

        assertEquals(10f, impl.getRadius(), 0f);
        assertEquals(12f, impl.getTopLeftRadius(), 0f);
        assertEquals(13f, impl.getTopRightRadius(), 0f);
        assertEquals(14f, impl.getBottomRightRadius(), 0f);
        assertEquals(15f, impl.getBottomLeftRadius(), 0f);
    }

    @Test
    public void testRadiusListLength_public() {
        RoundStatusImpl impl = new RoundStatusImpl();
        float[] r = impl.getRadiusList();
        assertEquals(8, r.length);
    }
}