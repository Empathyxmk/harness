package com.github.joonavali.naturalmouse.screenadjustednature;

import com.github.joonasvali.naturalmouse.support.ScreenAdjustedNature;
import com.github.joonasvali.naturalmouse.util.FactoryTemplates;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;

public class ScreenAdjustedNatureDefaultsPublicTest {
  @Test
  public void testDefaultSettingsForMediumSize_public() {
    ScreenAdjustedNature nature = new ScreenAdjustedNature(FactoryTemplates.basicRobotNature());
    // Defaults use 600x600
    int steps = nature.deriveSteps(0, 0, 325, 271);
    Assertions.assertTrue(steps > 0);
    Assertions.assertTrue(steps < 10000);
  }
}