package io.github.xiaofeidev.round.round;

import org.junit.Test;
import static org.junit.Assert.*;

public class RoundStatusImplBuilderPublicTest {

    @Test
    public void testBuilderSetsValues_public() {
        RoundStatusImpl.RoundStatusBuilder builder = new RoundStatusImpl.RoundStatusBuilder();
        builder.setMRadius(20.21f)
                .setMTopLeftRadius(22.22f)
                .setMTopRightRadius(23.23f)
                .setMBottomRightRadius(24.24f)
                .setMBottomLeftRadius(25.25f);

        RoundStatusImpl impl = builder.build();
        assertEquals(20.21f, impl.getRadius(), 0f);
        assertEquals(22.22f, impl.getTopLeftRadius(), 0f);
        assertEquals(23.23f, impl.getTopRightRadius(), 0f);
        assertEquals(24.24f, impl.getBottomRightRadius(), 0f);
        assertEquals(25.25f, impl.getBottomLeftRadius(), 0f);
    }
}