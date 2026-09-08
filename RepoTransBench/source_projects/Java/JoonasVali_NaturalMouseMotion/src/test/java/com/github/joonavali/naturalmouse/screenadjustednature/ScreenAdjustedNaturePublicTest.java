package com.github.joonavali.naturalmouse.screenadjustednature;

import com.github.joonasvali.naturalmouse.support.ScreenAdjustedNature;
import com.github.joonasvali.naturalmouse.util.FactoryTemplates;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.awt.*;

public class ScreenAdjustedNaturePublicTest {

  @Test
  public void testStepSizesConsistentOverWidth_public() {
    ScreenAdjustedNature sa = new ScreenAdjustedNature(FactoryTemplates.basicRobotNature());
    Dimension screen = new Dimension(380, 299);
    sa.setScreenSize(screen);

    int x1 = 2, x2 = 153, x3 = 364, y1 = 8, y2 = 199, y3 = 265;
    // All steps should be within new screen
    Assertions.assertTrue(sa.getMinSteps() < sa.getMaxSteps());
    int steps1 = sa.deriveSteps(x1, y1, x2, y1);
    int steps2 = sa.deriveSteps(x2, y2, x3, y2);
    Assertions.assertTrue(steps1 > 0 && steps2 > 0);
  }

  @Test
  public void testCharacteristicWithDifferentScreenSizes_public() {
    ScreenAdjustedNature sa = new ScreenAdjustedNature(FactoryTemplates.basicRobotNature());
    Dimension small = new Dimension(110, 99);
    Dimension large = new Dimension(1200, 1101);

    sa.setScreenSize(small);
    int stepsS = sa.deriveSteps(0, 0, 50, 30);
    sa.setScreenSize(large);
    int stepsL = sa.deriveSteps(0, 0, 800, 400);

    Assertions.assertTrue(stepsS < stepsL, "Steps on large screen should be more than small screen");
  }
}