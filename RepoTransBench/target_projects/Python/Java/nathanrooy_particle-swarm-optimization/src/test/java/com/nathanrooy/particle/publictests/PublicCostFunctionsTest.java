package com.nathanrooy.particle.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.nathanrooy.particle.CostFunctions;

public class PublicCostFunctionsTest {

    @Test
    public void testSphereAllZerosPublic() {
        assertEquals(0.0, CostFunctions.sphere(new int[]{0, 0, 0, 0}));
    }

    @Test
    public void testSphereSingleValuePublic() {
        assertEquals(16.0, CostFunctions.sphere(new int[]{4}));
    }

    @Test
    public void testSphereNegativeValuesPublic() {
        assertEquals(13.0, CostFunctions.sphere(new int[]{-3, -2}));
    }

    @Test
    public void testSphereMixedValuesPublic() {
        assertEquals(29.0, CostFunctions.sphere(new int[]{2, -3, 4}));
    }

    @Test
    public void testSphereEmptyPublic() {
        assertEquals(0.0, CostFunctions.sphere(new int[]{}));
    }

    @Test
    public void testMainGuardDoesNothingPublic() {
        assertNotNull(CostFunctions.class);
        assertDoesNotThrow(() -> CostFunctions.sphere(new int[]{}));
    }
}