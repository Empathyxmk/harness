package com.github.joonavali.naturalmouse.screenadjustednature;

import com.github.joonasvali.naturalmouse.support.ScreenAdjustedNature;
import com.github.joonasvali.naturalmouse.util.FactoryTemplates;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.awt.*;

public class ExtendedScreenPublicTest {
  @Test
  public void testRangeOfMotionWithCustomScreen_public() {
    ScreenAdjustedNature nature = new ScreenAdjustedNature(FactoryTemplates.basicRobotNature());
    Dimension custom = new Dimension(1400, 970);
    nature.setScreenSize(custom);

    int dx = custom.width - 4;
    int dy = custom.height - 8;
    int minSteps = nature.deriveSteps(0, 0, dx, dy);
    Assertions.assertTrue(minSteps > 100);
    Assertions.assertTrue(minSteps < 20000);
  }
}