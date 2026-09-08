package com.nathanrooy.particle.publictests;

import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.*;
import com.nathanrooy.particle.PsoSimple;
import com.nathanrooy.particle.CostFunctions;
import java.util.*;

public class PublicPsoTest {

    @Test
    public void testMinimizeWithSphereFunctionPublic() {
        double[] x0 = {-2.0, 3.0};
        double[][] bounds = {{-10, 10}, {-10, 10}};
        Object[] result = PsoSimple.minimize(CostFunctions::sphere, x0, bounds, 5, 12, false);
        double err = (double) result[0];
        @SuppressWarnings("unchecked")
        List<Double> pos = (List<Double>) result[1];
        assertTrue(err <= CostFunctions.sphere(x0));
        assertEquals(x0.length, pos.size());
    }
}