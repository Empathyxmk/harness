package io.github.xiaofeidev.round.round;

import org.junit.Test;
import static org.junit.Assert.*;

public class RoundStatusImplBuilderTest {

    @Test
    public void testBuilderChain() {
        RoundStatusImpl.RoundStatusBuilder builder = new RoundStatusImpl.RoundStatusBuilder();
        builder.setMRadius(9f)
               .setMTopLeftRadius(8f)
               .setMTopRightRadius(7f)
               .setMBottomLeftRadius(6f)
               .setMBottomRightRadius(5f);

        RoundStatusImpl impl = builder.build();
        assertEquals(9f, impl.getRadius(), 0.00001f);
        assertEquals(8f, impl.getTopLeftRadius(), 0.00001f);
        assertEquals(7f, impl.getTopRightRadius(), 0.00001f);
        assertEquals(6f, impl.getBottomLeftRadius(), 0.00001f);
        assertEquals(5f, impl.getBottomRightRadius(), 0.00001f);
    }
}