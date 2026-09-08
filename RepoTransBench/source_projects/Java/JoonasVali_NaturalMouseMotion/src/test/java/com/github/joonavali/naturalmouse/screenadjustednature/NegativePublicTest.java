package com.github.joonavali.naturalmouse.screenadjustednature;

import com.github.joonasvali.naturalmouse.support.ScreenAdjustedNature;
import com.github.joonasvali.naturalmouse.util.FactoryTemplates;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import java.awt.*;

public class NegativePublicTest {
  @Test
  public void testNegativeCoordinates_public() {
    ScreenAdjustedNature nature = new ScreenAdjustedNature(FactoryTemplates.basicRobotNature());
    Dimension d = new Dimension(500, 400);
    nature.setScreenSize(d);
    int steps = nature.deriveSteps(-15, -10, 100, 50);
    Assertions.assertTrue(steps > 0);
  }
}