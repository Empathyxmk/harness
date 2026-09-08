package io.github.xiaofeidev.round.round;

import org.junit.Test;

public class RoundStatusTest {
    @Test
    public void testInterfaceIsImplemented() {
        RoundStatus obj = new RoundStatusImpl();
        obj.setRadius(7.2f);
        obj.setTopLeftRadius(2.2f);
        obj.setTopRightRadius(3.2f);
        obj.setBottomLeftRadius(4.2f);
        obj.setBottomRightRadius(5.2f);

        obj.fillRadius();
        obj.getBottomLeftRadius();
        obj.getBottomRightRadius();
        obj.getRadius();
        obj.getRadiusList();
        obj.getTopRightRadius();
        obj.getTopLeftRadius();
    }
}